---
layout:	post
title:	"Memory Leak"
tag: 编程
date:	2015-03-08
---

工具：
LeakFinderC.exe

用法：
LeakFinderC dumpFile leakCandidateFile symbolFile [falseAlarmFile]

常见错误：

+ 赋值过程中拷贝了2次但只有一个指针：

{%highlight C++%}
inline BSTR MsiString2BSTR(const MBase::String& String)
{
	return SysAllocString(String.c_str());	//copied once
}

class CComBSTR
{
public:
	BSTR m_str;
	CComBSTR()
	{
		m_str = NULL;
	}
	/*explicit*/ CComBSTR(Int32 nSize)
	{
		m_str = ::SysAllocStringLen(NULL, nSize);
	}
	/*explicit*/ CComBSTR(Int32 nSize, LPCOLESTR sz)
	{
		m_str = ::SysAllocStringLen(sz, nSize);
	}
	/*explicit*/ CComBSTR(LPCOLESTR pSrc)
	{
		m_str = ::SysAllocString(pSrc);	//copied twice
	}
	/*explicit*/ CComBSTR(const CComBSTR& src)
	{
		m_str = src.Copy();
	}
	/*explicit*/ CComBSTR(REFGUID src)
	{
		LPOLESTR szGuid;
		StringFromCLSID(src, &szGuid);
		m_str = ::SysAllocString(szGuid);
		CoTaskMemFree(szGuid);
	}
	CComBSTR& operator=(const CComBSTR& src)
	{
		if (m_str != src.m_str)
		{
			if (m_str)
				::SysFreeString(m_str);
			m_str = src.Copy();
		}
		return *this;
	}

	CComBSTR& operator=(LPCOLESTR pSrc)
	{
		::SysFreeString(m_str);
		m_str = ::SysAllocString(pSrc);
		return *this;
	}

	~CComBSTR()
	{
		::SysFreeString(m_str);
	}
	
	operator BSTR() const
	{
		return m_str;
	}
	BSTR* operator&()
	{
		return &m_str;
	}
	
	void Attach(BSTR src)
	{
		if (m_str != src)
		{
			::SysFreeString(m_str);
			m_str = src;
		}
	}
	BSTR Detach()
	{
		BSTR s = m_str;
		m_str = NULL;
		return s;
	}
};

CComBSTR lFileEncodingBSTR = MsiString2BSTR(lFileEncoding);

{%endhighlight%}

+ 由于某些原因新加的代码导致原有的申请空间没有被释放

{%highlight C++%}

HRESULT CDSSEvaluationPU::Init()
{
	...
}

STDMETHODIMP CDSSDataSource::Reset()
{
	...
	switch (mMode)	//missing a case here so mpEvalPU.Release() is never invoked 
	{
		case xxx:
			...
			break;
		...
		default:
			return TRACE_LEAVE();
	}
	...
	mpEvalPU.Release();
	return TRACE_LEAVE;
}
{%endhighlight%}

+ 虽然改好了，但看不出原因。。。(should be a false alarm?)

{%highlight C++%}

//MContractMgr::CreateContractManagerInstance();
//MDb::ContractManagerPtr lContractManagerPtr(new DSSDbContractManager(100*1024*1024, MContractMgr::ContractManagerInstance())); 

MDb::ContractManagerPtr lContractManagerPtr(new DSSDbContractManager(100*1024*1024, MContractMgr::CreateContractManagerInstance())); 	//Memory leak happens in the above two lines!! Comment them out and use this line fixes this leak 


namespace MBase 
{
	class ReferenceCounted
	{
	protected:

		virtual ~ReferenceCounted() throw()
		{
		};

	public:
		virtual void AddRef() const throw()=0;
		virtual void Release() const throw()=0;
	};
}

namespace MContractMgr {

class ContractManager : public MBase::ReferenceCounted
{
public:
	// Reserve returns a "handle" of the memory reserved (to be used in unreserve)
	virtual unsigned Int32 InitiateContract(const _TCHAR* ipcSource)=0;
	virtual void CancelContract(unsigned Int32 inHandle) throw()=0;

	virtual MCMRESULT Reserve(unsigned Int32 inHandle,unsigned Int32 inSize,unsigned Int32 inTimeout)=0;
	//NC- None-continuous version. The reserved memory is not necessarily continuous
	//The size could be > 4GB and in Int64 type
	virtual MCMRESULT ReserveNC(unsigned Int32 inHandle,unsigned Int64 inSize,unsigned Int32 inTimeout,bool ibContinuous = true)=0;
	virtual void UnReserve(unsigned Int32 inHandle,unsigned Int32 inSize) throw()=0;
	//NC- None-continuous version. The size is 64 bit.
	virtual void UnReserveNC(unsigned Int32 inHandle,unsigned Int64 inSize) throw()=0;
	
	virtual void SetMemoryCounters(MemoryStatus::MemoryCounters &irMemoryCounters)=0;
};

typedef MBase::SmartPtrI<ContractManager> ContractManagerPtr;
DLL_CONTRACTMGR_EXIM ContractManager* CreateContractManagerInstance();
DLL_CONTRACTMGR_EXIM ContractManager* ContractManagerInstance();

}

ContractManager* CreateContractManagerInstance()
{
#if defined WIN32
#ifdef SMARTHEAP
	return ContractManagerImplSHNT::CreateInstance();
#else
	return ContractManagerImplNT::CreateInstance();
#endif
#elif defined sun
	return ContractManagerImplSolaris::CreateInstance();
#elif defined _AIX
	return ContractManagerImplAIX::CreateInstance();
#elif defined(linux) || defined(__APPLE__)
	return ContractManagerImplLinux::CreateInstance();
#elif defined __hpux
	return ContractManagerImplHPUX::CreateInstance();
#else
#error	unsupported platform
#endif
}

ContractManagerImplNT* ContractManagerImplNT::CreateInstance()
{
	if(mpContractManager.IsNull())
	{
		mpContractManager = new ContractManagerImplNT();
		_ASSERT(!mpContractManager.IsNull());
		if (!mpContractManager.IsNull()) {
			if (!mpContractManager->InitMCM()) {
				_ASSERT(false);
				mpContractManager.Reset();
			}
		}
	}

	return mpContractManager.Get();
}

ContractManager* ContractManagerInstance()
{
#if defined WIN32
#ifdef SMARTHEAP
	return ContractManagerImplSHNT::Instance();
#else
	return ContractManagerImplNT::Instance();
#endif
#elif defined sun
	return ContractManagerImplSolaris::Instance();
#elif defined _AIX
	return ContractManagerImplAIX::Instance();
#elif defined(linux) || defined(__APPLE__)
	return ContractManagerImplLinux::Instance();
#elif defined __hpux
	return ContractManagerImplHPUX::Instance();
#else
	#error "Unsupported platform"
#endif
}

ContractManagerImplNT* ContractManagerImplNT::Instance()
{
	return mpContractManager.Get();
}

namespace MDb
{
	/**
	 * MDb::ContractManager is the interface that the db classes will use to create memory contracts.
	 * The application using the db classes must provide the MDb::ConnectionManager with an object that
	 * implements this interface in order to enable contract manager in the db classes.
	 */
	class ContractManager: public MBase::ReferenceCounted
	{
	public:
		virtual MBase::ReturnPtrI<MBase::MemoryContract> CreateMemoryContract(wchar_t* ipSource) = 0;

		virtual unsigned int GetMaximumOutOfProcessTableSize() = 0;
	};

	typedef MBase::SmartPtrI<ContractManager> ContractManagerPtr;

} // namespace

class DSSDbContractManager: public MDb::ContractManager
{
public:
	DSSDbContractManager(unsigned int iMaximumOutOfProcessTableSize, 
		MContractMgr::ContractManager* ipContractManager);
	virtual ~DSSDbContractManager() throw();

	MBase::ReturnPtrI<MBase::MemoryContract> CreateMemoryContract(wchar_t* ipSource);

	unsigned int GetMaximumOutOfProcessTableSize();

	REFERENCE_COUNTED_IMPLEMENTATION
private:
	const unsigned int mMaximumOutOfProcessTableSize;
	MContractMgr::ContractManagerPtr const mpContractManager;
};

DSSDbContractManager::DSSDbContractManager(unsigned int iMaximumOutOfProcessTableSize, 
										   MContractMgr::ContractManager* ipContractManager):
	mMaximumOutOfProcessTableSize(iMaximumOutOfProcessTableSize),
	mpContractManager(ipContractManager)
{
	_ASSERTE(ipContractManager);
}

namespace MBase
{
	template<class ReferenceCountedT>
	class SmartPtrI
	{
	public:
		SmartPtrI(ReferenceCountedT* ipData=NULL) throw() :
		  mpData(ipData)
		{
			if(mpData)
			{
				mpData->AddRef();
			}
		}

		// copy constructor allowed on SmartPtr
		// upcast should be implicit
		template<class ReferenceCountedU>
		SmartPtrI(const SmartPtrI<ReferenceCountedU>& irSmartPtrI) throw()
		{
			if (!irSmartPtrI.IsNull())
			{
				mpData = irSmartPtrI.Get();
				mpData->AddRef();
			}
			else
			{
				mpData = NULL;
			}
		}

		SmartPtrI(const SmartPtrI<ReferenceCountedT>& irSmartPtrI) throw()
		{
			if (!irSmartPtrI.IsNull())
			{
				mpData = irSmartPtrI.Get();
				mpData->AddRef();
			}
			else
			{
				mpData = NULL;
			}
		}

		~SmartPtrI() throw()
		{
			Dispose();
		}

		void Reset(ReferenceCountedT* ipData=NULL) throw()
		{
			if(mpData!=ipData)
			{
				Dispose();
				mpData=ipData;
				if(mpData)
				{
					mpData->AddRef();
				}
			}
		}

		// Attach to a raw pointer without AddRef
		void Attach(ReferenceCountedT* ipData=NULL) throw()
		{
			Dispose();
			mpData=ipData;
		}

		// Assignment operator of raw pointer
		// upcast should be implicit
		SmartPtrI& operator=(ReferenceCountedT* ipData) throw()
		{
			Reset(ipData);
			return *this;
		}

		// Assignment operator
		// upcast should be implicit
		template<class ReferenceCountedU>
		SmartPtrI& operator=(const SmartPtrI<ReferenceCountedU>& irSmartPtrI) throw()
		{
			if (!irSmartPtrI.IsNull())
			{
				Reset(irSmartPtrI.Get());
			}
			else
			{
				Reset(NULL);
			}
			return *this;
		}

		SmartPtrI& operator=(const SmartPtrI<ReferenceCountedT>& irSmartPtrI) throw()
		{
			if (!irSmartPtrI.IsNull())
			{
				Reset(irSmartPtrI.Get());
			}
			else
			{
				Reset(NULL);
			}
			return *this;
		}

		// Assignment operator from a return ptr
		// upcast should be implicit
		template<class ReferenceCountedU>
		SmartPtrI& operator=(ReturnPtrI<ReferenceCountedU>& irReturnPtrI) throw()
		{
			// do not add ref again, "steal" the reference from the return ptr
			Reset(NULL);
			mpData=irReturnPtrI.GiveUp();
			return *this;
		}

		ReferenceCountedT* operator->() const throw()
		{
			_ASSERTE(mpData!=NULL);
			return mpData;
		}

		ReferenceCountedT& operator*() const throw()
		{
			_ASSERTE(mpData!=NULL);
			return *mpData;
		}

		ReferenceCountedT* Get() const throw()
		{
			return mpData;
		}

		bool IsNull() const throw()
		{
			return !mpData;
		}

		template<class ReferenceCountedU>
		void DownCastFrom(SmartPtrI<ReferenceCountedU>& irSmartPtrI) throw()
		{
			// Only modify if iData is different from the current member
			if(static_cast<ReferenceCountedU*>(mpData) != irSmartPtrI.Get())
			{
				Reset(reinterpret_cast<ReferenceCountedT*>(irSmartPtrI.Get()));
			}
		}

		bool operator==(const SmartPtrI& iSmartBase) const
		{
			return mpData==iSmartBase.mpData;
		}

		bool operator<(const SmartPtrI& iSmartBase) const
		{
			return mpData<iSmartBase.mpData;
		}

		// GiveUp will relinquish this reference to the object
		// (we will not call release when it goes out of scope)
		ReferenceCountedT* GiveUp() throw()
		{
			ReferenceCountedT* lpTemp=mpData;
			mpData=NULL;
			return lpTemp;
		}

		// implicit cast to return ptr (to allow user to just call "return SmartPtrI")
		operator ReturnPtrI<ReferenceCountedT>() const
		{
			return Return();
		}

		// create a ReturnPtrI from this smart ptr
		// this will increment the reference count by 1 (upon creating the return ptr)
		ReturnPtrI<ReferenceCountedT> Return() const
		{
			return ReturnPtrI<ReferenceCountedT>(mpData);
		}
	private:
		void Dispose() throw()
		{
			//To avoid problems with circular references make a temporary
			//copy first and set the member to the new one before deleting it
			ReferenceCountedT* lpDataTemp = mpData;
			if(lpDataTemp)
			{
				mpData=NULL;
				lpDataTemp->Release();
			}
		}
		ReferenceCountedT* mpData;
	};
}
{%endhighlight%}

几点感想：

1. Smart point is not silver bullet. 其实它并没有解决问题，只是转移了问题。

2. 用智能指针其实更具迷惑性。因为智能指针本身也要申请内存。这样我们除了要关注智能指针包含的指针的内存管理，还要留意智能指针本身申请的内存什么时候释放

3. 用了智能指针程序可读性更差
