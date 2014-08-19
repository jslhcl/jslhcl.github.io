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
But we need to be pratical about standards. We can't just say all you need are lambdas -- Alonzo Church proved it, so we're not going to add any more to the language.

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
