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

**To prove that you are human, please complete this [assessment](https://www.youtube.com/watch?v=dQw4w9WgXcQ) first.**

Once done, please proceed to the writeup below. 
Thank you.

---

# CAPTCHAs

Having used the internet for over 14 years, CAPTCHAs can be just as annoying as pop-up ads when you lack a decent adblocker.
Sure, CAPTCHAs can be annoying, but they actually stop those pesky bots from disguising themselves as real users.

This helps keep websites running smoothly and prevents you from experiencing slow, frustrating service.
But having to solve them every single time, especially on brand new sites, can be incredibly frustrating.

## Why it only works on the surface level

CAPTCHAs does not even work (when looking at every possible ways to bypass CAPTCHAs).

Sure, CAPTCHAs aren't perfect.
A determined attacker with enough resources could probably crack them eventually.

Take this simple multiplayer [game](https://agar.io).
They added CAPTCHAs to fight the growing problem of bots trying ruin the game for everyone.

Every now and then, you get hit with a CAPTCHA test just to spawn into the game.
Frustrating, right?

Moneyclip's— err, Miniclip's goal was to prevent bots from overwhelming the game server.
However, that doesn't seem to be working, as there are still bots present in the game.

Anyone can simply reuse a valid CAPTCHA token or response to spawn bots and start causing disruptions.
People just keeps finding ways to bypass CAPTCHAs.

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

Well, buckle up and get ready to **re-enjoy** the CAPTCHA test once again!
Maybe it's just a matter of honing your skills in identifying blurry storefronts at lightning speed.
Definitely a skill issue.

*What if I am actually a robot?*

*Should I stop poking around `robots.txt`?*

*Or could it be my proxy or VPN is the cause?*

*Nada, it's the fault of the captcha.*
It has to be.

## But muhh server!

A rumor has been circulating that half of the internet's users might actually be robots.
There's no way to definitively confirm or deny this claim at this point.
Okay, maybe it's [true](https://www.imperva.com/resources/resource-library/reports/2023-imperva-bad-bot-report/).

From a developer's perspective, CAPTCHAs serve as an effective deterrent against brute-force attacks on websites, while also thwarting spammers and bots.
This simple yet powerful tool stands as a frontline defense against malicious activity in the digital realm.

CAPTCHAs do the job for smaller web servers and those online shops that aren't equipped to handle a barrage of traffic.
However, even determined botters can still slide past them.
And believe it or not, even the least tech-savvy folks can sometimes bypass CAPTCHAs.

For example, you can install [buster](https://github.com/dessant/buster) as a browser extension.

![buster](./buster1.png)

Then, select buster's icon to bypass Google's reCAPTCHA.
Easy, right?

What buster did was use artificial intelligence to bypass the audio test by using speech-to-text recognition.

![Audio Bypass](./audio.png)

This attack was pretty clever.
It exploited the accessibility features built into CAPTCHAs.
Those audio tests they have for handicapped people.
Well, that's one way of bypassing the whole CAPTCHA test by focusing on that audio test.

Similarly, there is a method for Cloudflare's hCaptcha.
It's not a bypass since Cloudflare is the one who made them but at least the test is no longer an annoyance.
It's called [Privacy Pass](https://blog.cloudflare.com/privacy-pass-standard).

However, there is method that's guaranteed to always work.
And that is by hiring digital slaves for a cheap price.
This is accomplished by letting hundreds of slav- I mean paid workers or "freelancers" to solve the CAPTCHA test for you.

It works too well even on Cloudflare's hCaptcha and not just on Google's reCAPTCHA.
It would even work on other CAPTCHAs as well.
If you have seen job postings that mentions _Work passively anytime!_, _Earn money by typing!_, or _Easy money in X hours!_ (non-verbatim), that is what those services that provides mitigations to CAPTCHAs.
By offering a paid service, they do the work for you.

On the other hand, Phishing websites would have issues with bots, 100% guaranteed.
All they could do is block a certain IP address.
Yet, if they implement CAPTCHA on their server, their automation tool to send usernames and passwords would be useless.

It is quite funny to see phishing sites gets blasted with random username and passwords.
They deserve it well.

## This writeup is definitely not written by a bot

Okay, so there are good and there bad for CAPTCHAs.
But we still hate them.
Since there are now more bots than humans, CAPTCHA is a requirement.

*So, are CAPTCHAs worth it?*
Eh, it really depends on which point of view we are looking at.
If majority uses CAPTCHAs to deter bots, spammers, and bruteforce attacks then they are worth it as the owner of a service.
But as a user?
It's an annoyance and sometimes may not be worth it.
For us, it's not worth it.

*Is it more trouble than it is worth?*
As a developer, no.
As a user, yes.
But over time, users would just accept the fact that CAPTCHAs are part of the internet and becomes ingrained with them.
Making the pain a part of browsing the internet.
I am a user and unfortunately CAPTCHAs has grown on me.

---

Basically, CAPTCHAs are annoying but it's like a requirement on the internet.
Just like having an ad blocker is a requirement to surf the web (UBlock Origin ftw).

We have no choice but to cope with CAPTCHAs because malicious people can't stop being malicious.
However, we have the freedom to use the website or just stop accessing it.
Yet that's still not considered having a choice...
