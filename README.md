# Instructions
1. Install Tor expter bundle ```https://www.torproject.org/download/tor/```
2. Find your torrc file and edit in
```
ControlPort 9051
CookieAuthentication 1
HashedControlPassword PASSWORD
```

If you don't know how to get a password, open CMD as admin and type this in with "your_new_password" being your password `tor --hash-password your_new_password`

3. Save it
4. open CMD as admin in the tor folder and run ```tor --SocksPort 9050 --ControlPort 9051```
5. Once it says ```Bootstrapped 100% (done): Done``` your server is established and ready to go!

Just make sure the the tor server is running first before you run the program!
