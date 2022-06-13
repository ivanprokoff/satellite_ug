import datetime

import vk_api
import schedule
import time


vk_session = vk_api.VkApi(token='vk1.a.XADB7CyS1CEWa-Wi1G0S3tYN7iWEXJkvPvIA1RvQGWWpMJIs3onG65-khRbQhMpZRiSO3lCr29t-jhkjN2-8i5Jdy025P9x9Au3qjSLbpPjxJUWwOns_x9BTrgp4kzqaKZt5hg_diLcSraui6oe7PavDcBIRq_AXfp0vWHJvUQFdnoKR9xZG1g_Nf-NHeVux')


def send_message():
    dtm = datetime.datetime(2022, 6, 14, 23, 59, 59, 999999)
    dtm1 = datetime.datetime.now()
    delta = dtm - dtm1
    sec = delta.seconds
    hour = sec // 3600
    sec = sec % 3600
    mins = sec // 60
    res = f"[BOT] Максимальное время до окончания ваши страданий: {delta.days} день, {hour} часов, {mins} минут, {sec % 60} секунд"
    vk_session.method('messages.send', {'chat_id': 260, 'message': res, 'random_id': 0})


#schedule.every(5).seconds.do(send_message)
schedule.every().hour.at(":00").do(send_message)
while True:
    schedule.run_pending()
    time.sleep(1)
