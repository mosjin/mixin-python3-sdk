# -*- coding: utf-8 -*-
"""
Mixin API TEST for Python 3.x
Base on: https://github.com/includeleec/mixin-python3-sdk,
Author: leec
env: python 3.x

Modified by mosjin
Website: jinLab.com
mixin: 1051676
update: 2020-02-14
"""
from mixin_api import MIXIN_API
from config import robot_config
import time
from config import mixin_asset_lists

mixin_api = MIXIN_API(robot_config)




transfer2user_id = 'b33b8e1a-ac41-40f4-8172-1fb5591f0895'  # mosjin user id

# cuiniubi token asset id

#test robot transfer to user_id
for i in range(1, 5):
    r = mixin_api.transferTo(transfer2user_id, mixin_asset_lists.CNB_ASSET_ID, i /10000, "转账次数:" + str(i))
    time.sleep(1)

mixin_api.getTransfer('bc52ff5a-f610-11e8-8e2a-28c63ffad907')

# mixin_api.getTransfer('13f4c4de-f572-11e8-94cc-00e04c6aa167')
#
#
# mixin_api_robot.getAsset(mixin_asset_lists.CNB_ASSET_ID)
#
#
mixin_api.topAssets()
#
print('snapshot')
# mixin_api.snapshot('3565a804-9932-4c3c-8280-b0222166eec7')

# 289d6876-79ff-4699-9901-7a670953eef8
mixin_api.snapshot('289d6876-79ff-4699-9901-7a670953eef8')

