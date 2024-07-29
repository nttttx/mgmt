# Selfhosting

```sh
~> # Clone bot source code
~> git clone https://github.com/sillyheads/mgmt mgmt_bot
~> cd mgmt_bot
~/mgmt_bot> # Create venv
~/mgmt_bot> python3.11 -m venv .env
~/mgmt_bot> # Enter venv
~/mgmt_bot> source .env/bin/activate
~/mgmt_bot> pip install -r requirements.txt
~/mgmt_bot> cp config.example.json config.json
```

Now. Grab bot token from [@BotFather](https://t.me/BotFather).

Copy it and open `config.json` in your favourite editor. Replace "ur token" with your token.

Your `config.json` will look like this:
```json
{
  "BOT_TOKEN": "4839574812:AAFD39kkdpWt3ywyRZergyOLMaJhac60qc"
}  
```

Thats it!~ You're ready to run it!

```
~/mgmt_bot> python -m mgmt_bot
```
