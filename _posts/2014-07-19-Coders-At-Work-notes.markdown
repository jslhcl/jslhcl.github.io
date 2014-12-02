---
layout:	post
title:	"Coders At Work notes"
date:	2014-07-19
---
# Jamie Zawinski
At the end of the day, ship the fucking thing! It's great to rewrite your code and make it cleaner and by the third time it'll actually be pretty. But that's not the point -- you're not here to write code; you're here to ship products.

If you spend the time to build the perfect framework that's going to do what you want and that's going to carry you from release 1.0 through release 5.0 and everything's going to be great; well guess what: release 1.0 is going to take you three years to ship and your competitor is going to ship their 1.0 in six months and now you're out of the game. Your never shipped your 1.0 because someone else ate your lunch.

Your competitor's six-month 1.0 has crap code and they're going to have to rewrite it in two years but, guess what: they can rewrite it because you don't have a job anymore.

...if we'd had unit tests or smaller modules or whatever. That all sounds great in principle. Given a leisurely development pace, that's certaintly the way to go. But when you're looking at, "We've got to go from zero to done in six weeks", well, I can't do that unless I cut something out...I hope I don't sound like I'm saying "Testing is for chumps", it's not. It's a matter of priorities. Are you trying to write good software or are you trying to be done by next week? You can't do both.

...Design Patterns -- which I just thought was crap...Then in meetings they'd be tossing around all this terminology they got out of that book. Like, the inverse, reverse, double-back-flip pattern -- whatever. Oh, you mean a loop? OK.

# Brendan Eich
But we need to be practical about standards. We can't just say all you need are lambdas -- Alonzo Church proved it, so we're not going to add any more to the language.

# Joshua Bloch
But what you do is you force people to subset it (c++)

There are just a bunch of features (of c++) that you're not going to use because the resulting code is too high.

There's a brilliant quote by Tony Hoare in his Turing Award speech about how there are two ways to design a system: "One way is to make it so simple that there are obviously no deficiencies and the other way is to make it so complicated that there are no obvious deficiencies."

What we're doing is an aesthetic pursuit. It involves craftsmanship as well as mathematics and it involves people skills and prose skills -- all of these things that we don't necessarily think of as engineering but without which I don't think you'll ever be a really good enigneer. So I think it's just something that we have to remind ourselves of. But I think it's one of the most fun jobs on the planet. I think we're really lucky to have grown up at the time that we did when these skills led to these jobs. I don't know what we would have been doing a few generations back. 

# Joe Armstrong
I think the lack of reusability comes in object-oriented languages, not in functional languages. Because the problem with object-oriented language is they've got all this implicit environment that they carry around with them. You wanted a banana but what you got was a gorilla holding the banana and the entire jungle.

What I've learned is, programming when you're tired, you write crap and you throw it all away the next day.

I have noticed over the years, the really good code I would write was when I'm in complete flow -- just totally unaware of time: not even really thinking about the program, just sitting there in a relaxed state just typing this stuff and watching it come out on the screen as I type it in. That's code's going to be OK.

It's a movtivating force to implement something; I really recommand it. If you want to understand C, write a C compiler. If you want to understand Lisp, write a Lisp compiler or a Lisp interpreter.

Things you don't do are difficult and things you've done are easy.

Then there's -- I don't know if I read it somewhere or if I invented myself -- Joe's Law of Debugging, which is that all errors will be plus/minus three statements of the place you last changed the program.

I think the code is the answer to a problem. If you don't have the spec or you don't have any documentation, you have to guess what the problem is from the answer. You might guess wrong.

Do good stuff. If you don't do good stuff, in good areas, it doesn't matter what you do.

## Peter Norvig
I think one of the most important thing is being able to keep everything in your head at once. If you can do that you have a much better chance of being successful. That maks a small program easier.

One of the most important things for having a successful project is having people that have enough experience that they build the right thing. And barring that, if it's something that you haven't built before, that you don't know how to do, then the next best thing you can do is to be flexible enough that if you build the wrong thing you can adjust.

## Dan Ingalls
Although I didn't go very far, my conclusion was that it isn't that young people learn that much faster; it's just they have more time. When I would put time in, I made progress.

## L Peter Deutsch
The old idea of program correctness was that there were these assertions that were your expressions of what you intend the code to do in a way that was mechanically checkable against the code itself. There were lots of problems with that approach. I now think that the path to software that's more likely to do what we intend it to do lies not through assertions, or inductive assertions, but lies through better, more powerful, deeper declarative notations. 

Language systems stands on a tripod. There's the language, there's the libraries, and there are the tools. And how successful a language is depends on a complex interaction between those three things.

## Ken Thompson
Modern programming scares me in many respects, where they will just build layer after layer after layer that does nothing except translate. It confuses me to read a program which you must read top-down. It says "do something." And you go find "something." And you read it and it says "do something else" and you go find something and it says, "do something else" and it goes back to the top maybe. And nothing gets done. It's just relegating the problem to a deeper and deeper level.

You should do well but not really good. And the reason is that in the time it takes you to go from well to really good, Moore's law has already surpassed you. You can pick up 10 percent but while you're picking up that 10 percent, computers have gotten twice as fast and maybe with some other stuff that matters more for optimization, like caches. I think it's largely a waste of time to do really well. It's really hard; you generate as many bugs as you fix. You should stop, not take that extra 100 percent of time to do 10 percent of the work.

## Fran Allen
One could never really write specs that were going to be adequate and useful at a detail level over the years of the life circle. That was a problem. And now we have another process, of course--just do it and throw it away, kind of.

## Donald Knuth
The scientist gets older and says, "Oh, yes, some of the things that I've been doing have a really great payoff and other things, I'm not using anymore. I'm not going to have my students waste time on the stuff that doesn't make giant steps. I'm not going to talk about low-level stuff at all. These theoretical concepts are really so powerful -- That's the whole story. Forget about how I got to this point."
I think that's a fundamental error made by scientists in every field. They don't realize that when you're learning something you've got to see something at all levels. You've got to see the floor before you build the ceiling. That all goes into the brain and gets shoved down to the point where the older people forget that they needed it.

I think programming is a lot like religion; people have their beliefs. Some people like to force their beliefs on others.

The first rule of writing is to understand your audience -- the better you know your reader the better you can write, of course. The second rule, for technical writing, is say everything twice in complementary ways so that the person who's reading it has a chance to put the ideas into his or her brain in ways that reinforce each other.

The problem is that coding isn't fun if all you can do is call things out of a library, if you can't write the library yourself. If the job of coding is just to be finding the right combination of parameters, that does fairly obvious things, then who'd want to go into that as a career?

On one hand you have this impossibility of ever having something proved. Somebody will say they have a program that's verified and it's only verified because it met its specifications according to some verifier. But the verifier might have a bug in it. The specifications might have bugs in them. So you never know that the program is correct. You have more reason to believe it, but you never get to the end of the loop. It's theoretically impossible.

========
## 几点感想

貌似也没几个人从头到尾读过TAOCP

如何判断一个人是不是优秀的程序员，基本都是靠感觉。

程序证明这种事情工业届真的会去执行吗？preconditions, postconditions, 一个应用程序那么多函数，放在哪一层合适？

对Literate programming也有同样的疑问。

Knuth不愧“述而不作，信而好古”的名士风范
