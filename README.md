# Instructions
1. Install Tor expter bundle ```https://www.torproject.org/download/tor/```
2. Find your torrc file and edit in
```
ControlPort 9051
CookieAuthentication 1
HashedControlPassword PASSWORD
```

If you don't know how to get a password, open CMD as admin and type this in with "your_new_password" being your password `tor --hash-password your_new_password`

3. It's going to output a long string that starts with ```16:``` and then continues with a long list of characters that are capital letters and numbers.
4. Save the password and input it into the code and torrc file.
5. open CMD as admin in the tor folder and run ```tor --SocksPort 9050 --ControlPort 9051```
6. Once it says ```Bootstrapped 100% (done): Done``` your server is established and ready to go!

Just make sure the tor server is running first before you run the program!
