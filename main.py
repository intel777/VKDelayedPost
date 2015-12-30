import datetime, time, vk, json, requests as r

token = input('access_token: ')
session = vk.AuthSession(access_token=token)
api = vk.API(session)
api.stats.trackVisitor()

needed_datetime = input('Введите дату в формате "HH:MM:SS DD:MM:YY": ')

screen_name = input('Введите короткую ссылку пользователя/группы: ')
result = api.utils.resolveScreenName(screen_name=screen_name)
if result['type'] == 'group':
    wall_id = '-{}'.format(result['object_id'])
    print('Detected: Group, {}'.format(wall_id))
else:
    wall_id = result['object_id']
    print('Detected: User, {}'.format(wall_id))

content = input('Введите текст поста: ')
attachments = input('Какие-нибудь вложения?[Y/n]: ')
if attachments == 'Y':
    attachment_dir = input('Название картинки(должна лежать радом с этим файлом): ')
    upload = api.photos.getWallUploadServer(owner_id = wall_id)
    files = {'photo': ('{}'.format(attachment_dir), open(r'{}'.format(attachment_dir), 'rb'))}
    url = upload['upload_url']
    data={"aid":upload['aid'],
          "mid":upload['mid']
    }
    resp = r.post(url, data, files=files)
    response = json.loads(resp.text)

    method_url = 'https://api.vk.com/method/photos.saveWallPhoto?'
    if result['type'] == 'group':
        data = dict(access_token=token, gid=result['object_id'], photo=response['photo'], hash=response['hash'], server=response['server'])
    if result['type'] == 'user':
        data = dict(access_token=token, owner_id=result['object_id'], photo=response['photo'], hash=response['hash'], server=response['server'])
    response = r.post(method_url, data)
    result = json.loads(response.text)['response'][0]['id']

while True:
    now_time = datetime.datetime.now()
    cur_datetime = now_time.strftime("%H:%M:%S %d.%m.%y")
    if cur_datetime == needed_datetime:
        if attachments == 'n':
            api.wall.post(owner_id = wall_id, message = content)
        if attachments == 'Y':
            api.wall.post(owner_id = wall_id, message = content, attachment=result)
        print('Done!')
        time.sleep(10)
        exit()
