import yaml

from bot import MercStoriaBot

# botの接続と起動
# （tokenにはbotアカウントのアクセストークンを入れてください）
if __name__ == '__main__':
    env_config = None
    token = None
    try:
        with open('env.yaml', 'r') as stream:
            env_config = yaml.load(stream)
            token = env_config['discord']['token']
    except:
        # this var can setup in https://dashboard.heroku.com > Settings > Config Vars
        token = os.environ['DISCORD_BOT_TOKEN']

    bot = MercStoriaBot()
    bot.run(token)
