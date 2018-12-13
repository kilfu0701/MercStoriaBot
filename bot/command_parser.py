
AvaliableCommands = [
    'help',
    'list',
    'search',
    'show',
    'compare',
]

WordsGroup = {
    '屬性=炎': ['火', '炎', '火屬', '炎屬', '火屬性', '炎屬性', 'fire'],
    '屬性=水': ['水', '水屬', '水屬性', 'water'],
    '屬性=風': ['風', '風屬', '風屬性', 'wind'],
    '屬性=光': ['光', '光屬', '光屬性', 'bright'],
    '屬性=闇': ['暗', '暗屬', '暗屬性', '闇', '闇屬', '闇屬性', 'dark'],
    '武器種類=打撃': ['打', '打擊'],
    '武器種類=斬撃': ['斬', '斬擊'],
    '武器種類=突撃': ['突', '突擊'],
    '武器種類=弓矢': ['弓', '弓箭', '弓矢', 'arrow', 'bow'],
    '武器種類=魔法': ['魔', '魔法', '魔術', 'magic'],
    '武器種類=銃弾': ['銃', '銃弾', '槍', 'gun'],
    '武器種類=回復': ['補', '補師', '回復', 'priest', 'heal'],
    '國別': ['國別', '國', '國家', '国別', '国', '出身', '出身國', 'country', 'city'],
}

class CommandParser(object):

    def __init__(self, prefix='/merc'):
        self.prefix = prefix

    def parse(self, cmd_str):
        cmd_arr = cmd_str.strip().split(' ')

        # set default to 'help'
        cmd_type = 'help'
        if len(cmd_arr) > 1:
            if cmd_arr[1] in AvaliableCommands:
                cmd_type = cmd_arr[1]

        params = cmd_arr[2:]

        return cmd_type, cmd_arr[2:]

    def params_predict(self, params):
        pass
