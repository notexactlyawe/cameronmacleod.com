Title: How to configure DNS for custom domains on GitHub Pages
Date: 2018-11-20
Slug: github-pages-dns
Tags: Github Pages, DNS
Category: Tutorials

Recently-ish GitHub [announced](https://blog.github.com/2018-05-01-github-pages-custom-domains-https/) that HTTPS would now work on custom domains with GitHub Pages. This was a great bit of news, because the web is slowly moving towards a HTTPS-only state of being and it's nice not to be left behind.

Unfortunately for me, for this new feature to work you had to be using either **CNAME** or **ALIAS records** to point to your GitHub Pages domain. At the time, I was using **A records** pointed at the old GitHub Pages servers, which didn't have the new features enabled. All these terms can be quite confusing if you're not familiar with DNS, so let's take a look at some basics.

### What is DNS?

DNS stands for Domain Name System and it's the internet's way of mapping **URLs** (like `cameronmacleod.com`) to the actual **IP addresses** (like `185.199.108.153`) of the computers that can serve you the website. By means of an analogy, a **URL** is a bit like a postal address, for example:

 > 1 Castlehill  
 > Edinburgh  
 > EH1 2NG  
 > United Kingdom  

Unless you have been to Edinburgh, you would have no idea how to get to that address. You'd need something to take that address and give you directions back. Similarly, if you give a browser a **URL** then it would need something (in this case, a **nameserver**) to give it directions (an **IP address**) to find a website. Just as humans need directions to find a place, browsers need IP addresses to find a website.

DNS is the system by which these **URLs** are translated into **IP addresses**. For a basic mental model of how it works, you can think of these steps:

1. The **browser** asks a **nameserver** for the **IP address** related to a **URL**
2. The **nameserver** looks through some information it holds known as **records** to find out
3. The **nameserver** then tells the **browser** the **IP** and the **browser** goes away and fetches the website

A **nameserver** is just the DNS name for a computer that keeps **records** and can do the job of translating **URLs** to **IP addresses**.

This is not comprehensive or 100% accurate, but it's a good enough model for our purposes. If you would like to know more, or you're still a bit confused then Cloudflare have a [really good intro to the topic](https://www.cloudflare.com/learning/dns/what-is-dns/).

### What are DNS records?

So far, we know that things called **records** store the mapping between **URLs** and **IP addresses**. Presumably this means that if we want to make our site point at the GitHub Pages servers, then we need to change these. But what are **records** and how do they work?

At their core, **records** are just text files written in a certain way, that tell the **nameserver** how to find the **IP address** for a certain website. There are multiple different types of DNS **records** and all of them serve a slightly different purpose. Alongside the information below, all records have a `TTL` or `Time To Live` value that contains the number of seconds that the record is still valid for.

 - **A records** - These are possibly the simplest type of DNS records and hold the IP address for either a sub-domain (like `blog.cameronmacleod.com`) or your root domain (like `cameronmacleod.com`). Similarly, you may see **AAAA records** which are the same, but they hold an [IPv6 address](https://en.wikipedia.org/wiki/IPv6).

 - **CNAME records** - **CNAME** stands for **C**anonical **N**ame and points one domain name to another. The idea behind these records is to have a single official domain name and to let lots of other domains point to it. They are frequently used to redirect `www.` subdomains to the root domain. e.g. `www.cameronmacleod.com -> cameronmacleod.com`. They can only be used on sub-domains, not on root domains.

 - **ALIAS records** - These are similar to **CNAME records** in that they point your domain to another domain but there are a couple of subtle differences. **ALIAS records** can only be used on the root domain, not sub-domains, and they are not standardised across all DNS providers, so yours may or may not support them.

 - **Other record types** - There are many other record types, including **MX** for pointing to mail servers, **NS** for nameserver data and even **TXT** for general notes.

### How can I change my DNS records?

If you know your DNS provider already, then great! If not, you will need to either figure out which one you are using, or set one up if your site is not yet live. For those of you who have yet to set up DNS, often your domain name provider will have a DNS service as part of purchasing your domain name, if not then there are many free DNS providers out there.

If you (like me) can't remember what DNS provider you used, then a really useful tool can be found [from DNSstuff](https://www.dnsstuff.com/tools). On that page there is a "DNS Lookup" tool that you can type your domain into.

![DNS lookup tool screenshot](/images/dnsstufflookup.png)

On the page that follows, under the heading "Referral path:" you will see the words "Response from **some.dns.server**" where **some.dns.server** is your DNS server. You can then type that URL into Google and the results should tell you your provider.

![DNS lookup results screenshot](/images/dnslookupresults.png)

The actual process of changing your DNS records varies from provider to provider, but most will have an admin panel that you can log into and add/remove records. The records I have configured for my GitHub pages domain and by extension ones that should work for your GitHub Pages site are as follows:


Type   | Host name | Points to
-------|-----------|-----------
CNAME  | www       | notexactlyawe.github.io
ALIAS  |           | notexactlyawe.github.io

The first is necessary to redirect `www.cameronmacleod.com` to the GitHub Pages servers and the second redirects the "apex" domain (`cameronmacleod.com`).

When you come to configure this for yourself, you may find that there are no **ALIAS records** available under your provider. Unfortunately your best option in this case may be to change DNS provider.

### How do I know it worked?

DNS is notoriously slow to make changes to. Most providers recommend waiting 24 hours (some up to 72!) before you will be able to see your changes. When checking to see whether or not your changes have propagated, you can do one of two things. Use a DNS tool (like the one from [DNSstuff](https://www.dnsstuff.com/tools) above) or use the unix command `dig`.

`dig` is a command that can find and list the DNS records for a given domain name. On Linux and Mac machines, you can run the following in terminal:

```
cameron@isla:~$ dig www.cameronmacleod.com +noall +answer

; <<>> DiG 9.10.3-P4-Ubuntu <<>> www.cameronmacleod.com +noall +answer
;; global options: +cmd
www.cameronmacleod.com.	655	IN	A	192.30.252.154
www.cameronmacleod.com.	655	IN	A	192.30.252.153
```

The output might look a bit confusing, but it's the last two lines that count. Those are the records that `dig` has found for your domain. In my case, this output was from before I changed my DNS settings, so it still shows the old **A records** that I was using. Running it now would give something like this:

```
cameron@isla:~$ dig www.cameronmacleod.com +noall +answer

; <<>> DiG 9.10.3-P4-Ubuntu <<>> www.cameronmacleod.com +noall +answer
;; global options: +cmd
www.cameronmacleod.com.	3600	IN	CNAME	notexactlyawe.github.io.
notexactlyawe.github.io. 3599	IN	A	185.199.108.153
notexactlyawe.github.io. 3599	IN	A	185.199.109.153
notexactlyawe.github.io. 3599	IN	A	185.199.111.153
notexactlyawe.github.io. 3599	IN	A	185.199.110.153
```

You might notice that there are a lot of **A records**, but that is because **ALIAS records** will resolve automatically to **A records** in the DNS server, meaning that when you run `dig` it just shows you the final output.

You will want to check that the **IP addresses** in the last column of the `dig` output look similar to the ones above. For a complete and up to date list of GitHub Pages **IP addresses**, you can check [their documentation](https://help.github.com/articles/setting-up-an-apex-domain/#configuring-a-records-with-your-dns-provider).

If this worked, then great! Your DNS is properly configured to redirect your custom domain to GitHub Pages, and you should be able to visit your domain in a browser and see your page being served!

### HTTPS for custom domains in GitHub Pages

If you are trying to set up HTTPS on your site, then the changes above are necessary because they will point you at GitHub's content delivery network which has support for HTTPS. See [GitHub's announcement](https://blog.github.com/2018-05-01-github-pages-custom-domains-https/) for more details. You will also need to perform a couple more steps.

Firstly, if you used to be using **A records** then you may need to remove and re-add your custom subdomain from your repository's settings. This will generate you a certificate for your domain. To do this, firstly go to your repository settings.

![Screenshot of repository settings](/images/repositorysettings.png)

Next, head to the GitHub Pages settings and remove your domain from the "Custom domain" box and click "Save". Put your domain back in that box and click Save again.

![Screenshot of GitHub Pages settings](/images/githubpagessettings.png))

After doing this you will need to wait about an hour, but after that you should be able to go to `https://siteinthecustomdomainbox.com` and see a green padlock in the address bar. If the domain you put in the "Custom domain" box had a `www.` in front of it, then you will need to add that to the URL when visiting your site else it won't work.

For full and up to date instructions on the above see [GitHub's documentation](https://help.github.com/articles/adding-or-removing-a-custom-domain-for-your-github-pages-site/).

One thing to note is that HTTPS will only work for either `www.yoursite.com` or `yoursite.com` but not both depending on which one you put in the "Custom domain" box. GitHub are aware of the issue, but haven't given any public timeline for fixing it, see [this GitHub Community thread](https://github.community/t5/GitHub-Pages/Does-GitHub-Pages-Support-HTTPS-for-www-and-subdomains/td-p/7116).

# If something didn't work

GitHub have a really useful [troubleshooting guide](https://help.github.com/articles/troubleshooting-custom-domains/) for custom domains and HTTPS.
