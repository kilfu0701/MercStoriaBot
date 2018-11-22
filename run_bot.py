import yaml

from bot import MercStoriaBot

# botの接続と起動
# （tokenにはbotアカウントのアクセストークンを入れてください）

if __name__ == '__main__':
    env_config = None
    with open('env.yaml', 'r') as stream:
        env_config = yaml.load(stream)

    token = env_config['discord']['token']
    bot = MercStoriaBot()
    bot.run(token)
