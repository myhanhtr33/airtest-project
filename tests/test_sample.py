# coding=utf-8
import time
import pytest
from pocounit.case import PocoTestCase
from pocounit.addons.poco.action_tracking import ActionTracker
from pocounit.addons.hunter.runtime_logging import AppRuntimeLogging


class CommonCase(PocoTestCase):
    @classmethod
    def setUpClass(cls):
        super(CommonCase, cls).setUpClass()
    @pytest.fixture(scope="class")
    def setup_poco(cls,poco):
        cls.poco = poco
        action_tracker = ActionTracker(cls.poco)
        cls.register_addon(action_tracker)


class TestBuyShopItem(CommonCase):
    """
    去商城里把所有的道具都买一遍，验证所有道具都可以购买
    """

    def setUp(self):
        # 准备好足够的水晶和背包空间
        self.poco.command('***********')
        self.poco.command('***************************')

        # 清除掉每日购买次数限制
        self.poco.command('**********')

        # 打开商店界面
        if not self.poco('entry_list').exists():
            self.poco('switch_mode_btn').click()
        self.poco(text='商店').click()
        self.poco(textMatches='.*常规补给物资.*').click()

    def runTest(self):
        # 先买
        bought_items = set()
        bought_new = True
        while bought_new:
            bought_new = False
            for item in self.poco('main_node').child('list_item').offspring('name'):
                item_name = item.get_text()

                # 已经买过的就不再买了
                if item_name not in bought_items:
                    item.click()
                    self.poco(text='购买').click()
                    bought_items.add(item_name)
                    bought_new = True
                    item.click()

            # 向上卷动
            if bought_new:
                item_list = self.poco('main_node').child('list_item').child('list')
                item_list.focus([0.5, 0.8]).drag_to(item_list.focus([0.5, 0.25]))

        self.poco.dismiss([self.poco('btn_close')])

        # 再去背包验证
        self.poco('btn_bag').click()
        time.sleep(2)
        item_count = len(self.poco('bag_node').child('list').offspring('obj_frame_spr'))
        self.assertEqual(item_count, len(bought_items), '购买道具总数量验证')

    def tearDown(self):
        # 关掉界面
        self.poco.dismiss([self.poco('btn_close')])


if __name__ == '__main__':
    import pocounit
    pocounit.main()