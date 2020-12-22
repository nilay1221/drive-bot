# drive-bot
A Telegram Bot that uploads file to the drive.

# Prerequisite
Before working with Telegram’s API, you need to get your own API ID and hash:

1. [Login to your Telegram account](https://my.telegram.org/) with the phone number of the developer account to use.
2. Click under API Development tools.
3. A Create new application window will appear. Fill in your application details. There is no need to enter any URL, and only the first two fields (App title and Short name) can currently be changed later.
4. Click on Create application at the end. Remember that your API hash is secret and Telegram won’t let you revoke it. Don’t post it anywhere!

## Create your service account

1. Sign in to the Google API Console.
2. Open the Credentials page. If prompted, select the project that has the Android Management API enabled.
3. Click Create credentials > Service account key.
4. From the dropdown menu, select New service account. Enter a name for your service account.
5. Select your preferred key type and click Create. Your new public/private key pair is generated and downloaded to your machine and is the only copy of this key. You are responsible for storing it securely.

# How to Run

1. git clone `https://github.com/nilay1221/drive-bot.git`
2. cd `drive-bot`
3. Add your API ID , API HASH , BOT TOKEN in bot.py file.
4. Add Service Account Credentials file in current project directory and add its PATH in drive_upload.py
5. Add Shared Drive's id in drive_upload.py if using Shared Drive
6. Run `pip3 install -r requirements.txt`
6. Run `python3 bot.py`

# How to deploy on Heroku ?

1. Add your API ID , API HASH , BOT TOKEN in bot.py file.
2. Add Service Account Credentials file in current project directory and add its PATH in drive_upload.py
3. Add Shared Drive's id in drive_upload.py if using Shared Drive
4. RUN bot.py in your local machine to generate .session file
5. RUN these heroku commands
    1. `heroku create`
    2. `heroku container:login`
    3. `heroku container:push worker`
    4. `heroku container:release worker`
6. Your bot has been sucessfully deployed on heroku.


## Using Shared Drive

If you are using Shared Drive Id along with service account then you need to give permission to service account user by adding as a user in shared drive. After that only service account will be allowed to access shared drive Id.
    
