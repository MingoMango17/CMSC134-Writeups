---
title: CAPTCHAs
date: 2024-04-15
author:
  - "0x42697262"
  - Jinx
  - Orochi
---

Authors:

- 0x42697262
- Jinx
- Orochi

**To prove that you are human, please complete this [assessment](https://www.youtube.com/watch?v=dQw4w9WgXcQ) first.**[^1]

Once done, please proceed to the writeup below. 
Thank you.

---

# CAPTCHAs

Having used the internet for over 14 years, CAPTCHAs can be just as annoying as pop-up ads when you lack a decent adblocker.
Sure, CAPTCHAs are an annoyance, but they actually stop those pesky bots from disguising themselves as real users.

This helps keep websites running smoothly and prevents you from experiencing slow and frustrating service.
But having to solve them every single time, especially on brand new sites, can be incredibly infuriating.

## Why it only works on the surface level

CAPTCHAs do not even work (when looking at every possible ways to bypass CAPTCHAs).
Okay, that's a bold statement, certainly they "do work" but with a catch.

CAPTCHAs aren't perfect.
A determined attacker with enough resources could probably bypass them eventually.

For example, take this simple multiplayer [game](https://agar.io).
They added CAPTCHAs to fight the growing problem of bots trying ruin the game for everyone. And every now and then, you get hit with a CAPTCHA test just to spawn into the game.
Frustrating, right?

Moneyclip's— err, Miniclip's goal was to prevent bots from overwhelming the game server.
However, that doesn't seem to be working, as there are still bots present in the game.

Anyone can simply reuse a valid CAPTCHA token or response to spawn bots and start causing disruptions.
People just keep on finding ways to bypass CAPTCHAs.

**Granted, CAPTCHAs stop the super lazy cheaters from using bots, but the competent ones can still figure them out.**
Bummer, right?
It helps a bit to keep things fair, but it also makes things annoying for legit players who just wanna have fun.

The CAPTCHAs are a real pain, not just in games!
You try to do something quick online, and bam, you're stuck with one of those traffic light picture things.
Thirty seconds isn't so bad, but it's still annoying when you just want to get stuff done.

The worst part?
Having to do that counterproductive CAPTCHA thing **over and over** because apparently you didn't click the right fire hydrants the first time.
Come on, just let me log in already.

...And then you do it **again**, and **again**, and again.
It's like wasting your life away clicking on blurry buses for a good two or three minutes before you can finally get on with your day.
Yay! CAPTCHAs!

**And then there are those delightful moments** where you have to reload the entire page because the CAPTCHA session has expired and your hard-earned answers are no longer considered valid.

![Verification Failed](./expired.png)

Well, buckle up and get ready to **re-enjoy** the CAPTCHA joy-ride once again!
Maybe it's just a matter of honing your "skills" in identifying blurry storefronts at lightning speed.
Definitely a skill issue if you can't.

*What if I am actually a robot?*

*Should I stop poking around `robots.txt`?*

*Or could it be my proxy or VPN is the cause?*

*Nada, it's the fault of the captcha.*
It has to be.

Just why annoy your users?
And I mean the legit users.

Google, Facebook, Twitter, PopcornHub were able to do it without CAPTCHAs?
But not on certain websites that's poorly maintained.

Ah, yeah, it's because we've already sold our data to the internet conglomerates that they know well enough we're not bots.
Unlike websites that respects your privacy.

CAPTCHAs are only good enough to stop cheap tricks and whatnots.
A surface level of security.
Something something security is economics something.

## But muhh server!

A rumor has been circulating that half of the internet's users might actually be robots.
There's no way to definitively confirm or deny this claim at this point.
Okay, maybe it's [true](https://www.imperva.com/resources/resource-library/reports/2023-imperva-bad-bot-report/).

From a developer's perspective, CAPTCHAs serve as an effective deterrent against brute-force attacks on websites, while also thwarting spammers and bots.
This simple yet powerful tool stands as a frontline defense against malicious activity in the digital realm.

CAPTCHAs do the job for smaller web servers and those, but not limited to, online shops that aren't equipped to handle a barrage of traffic.
However, even determined botters can still slide past them.
And believe it or not, even the least tech-savvy folks can sometimes bypass CAPTCHAs.

For example, you can install [buster](https://github.com/dessant/buster) as a browser extension.
*Note that there are other free and open-source solutions as well.*

![buster](./buster1.png)

Then, select buster's icon to bypass Google's reCAPTCHA.
Easy, right?

What buster did was use artificial intelligence to bypass the audio test by using speech-to-text recognition.

![Audio Bypass](./audio.png)

This attack was pretty clever.
It exploited the accessibility features built into CAPTCHAs.

Those audio tests they have for handicapped people?
Well, that's one way of bypassing the whole CAPTCHA test by focusing on it.

Similarly, there is a method for Cloudflare's hCaptcha.
It's not a bypass since Cloudflare is the one who made them but at least the test is no longer an annoyance.
It's called [Privacy Pass](https://blog.cloudflare.com/privacy-pass-standard).

It's sort of like an attester that analyzes your browsing behaviour whether you're a bot or not.
I know I am not.

However, these method *does not work* most of the time for dedicated people that wants to overwhelm a server (maybe DDoS or spams?).
Audio verification won't work when CAPTCHAs can just analyze your browsing behavior.

Hence why there is method that's guaranteed to always work.
And that is by hiring digital slaves for a cheap price.
This is accomplished by letting hundreds of slav- I mean paid workers or "freelancers" to solve the CAPTCHA test for you.

This method works too well even on Cloudflare's hCaptcha and not just on Google's reCAPTCHA.
It would even work on other CAPTCHAs as well.

If you have seen job postings that mentions _Work passively anytime!_, _Earn money by typing!_, or _Easy money in X hours!_ (non-verbatim), that is what those services that provides mitigations to CAPTCHAs.
By offering a paid service, they do the work for you.

For certain "developers", phishing websites would have issues with bots, 100% guaranteed.
All they could do is block a certain IP address.
Yet, if they implement CAPTCHA on their server, their automation tool to send usernames and passwords would be useless, maybe.

It is quite funny to see phishing sites gets blasted with random username and passwords.
They deserve it well.

## CAPTCHA hell for normies

CAPTCHAs are not only annoying for the internet hermits out there, but are also hella annoying for those who are trying to browse the internet casually.

Imagine trying to log in to your favorite site after a long day at work, only to be greeted with a "Click on the traffic lights" CAPTCHA. Who wouldn't get annoyed at that?

Expending effort to finish the CAPTCHA, you are then notified that you need to verify again, making you want to scream.

Eventually, you succumb to this endless loop of CAPTHCAs that makes you want to pull your hair off.

Of course, the scenario above is highly exaggerated, but this is what countless casual internet users feel everytime when they meet with these CAPTCHAs that are  more forgiving when you are a bot than human.


## This writeup is definitely not written by a bot

Okay, so there is good and bad when we use CAPTCHAs.
But we still hate them.
And since there are now more bots than humans, CAPTCHA is inevitably a requirement.

*But that begs the question, are CAPTCHAs worth it?*

Eh, it really depends on which point of view we are looking at.
If majority uses CAPTCHAs to deter bots, spammers, and bruteforce attacks then they are worth it as the owner of a service.
But as a user?
It's an annoyance and sometimes may not be worth it.
For us, it's not worth it.

*Is it more trouble than it is worth?*

As a developer, no.
As a user, yes.
But over time, users would just accept the fact that CAPTCHAs are part of the internet and becomes a part of them.
Making the pain a part of browsing the internet.
I am a user and unfortunately CAPTCHAs has grown on me.

---

Basically, CAPTCHAs are annoying but it's like a requirement on the internet.
Just like having an ad blocker is a requirement to surf the web ([UBlock Origin](https://github.com/gorhill/uBlock) ftw).

We have no choice but to cope with CAPTCHAs because malicious people can't stop being... *malicious*.
But we do have the freedom to use the website or just stop accessing it.
Yet that's still not considered having a choice...

[^1]: If this takes you less than one minute to read, you're a bot.
