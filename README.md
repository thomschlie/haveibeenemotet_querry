##Short program to automatic querry E-Mails/Domains at www.haveibeenemotet.com
I wrote this program at work (Berlin-CERT). I needed to querry thousands of emails/domains with 
[www.haveibeenemotet.com](www.haveibeenemotet.com)
The program takes a list of email-addresses from file or stdin.

Returns a rows to stdout.
```
 EMAIL/DOMAIN  true/false  #NUM Real Sender    #NUM Fake Sender    #Num Recipient
```
true if in database, false if not