import time
class UIButtonUtils:
    @staticmethod
    def check_sprite_state(btn, expected_active,type_btn):
        sprite_map= {
            "btn_friend":"sFriend",
            "btn_add_friend":"sAddFriend",
            "btn_following":"sFollowing",
        }
        sprite_node= sprite_map.get(type_btn)
        sprite_btn=btn.child(sprite_node).attr("texture")
        active_sprite = "UI5_Friends_Tab_active"
        deactive_sprite = "UI5_Friends_Tab_off"
        if expected_active:
            return sprite_btn == active_sprite
        else:
            return sprite_btn == deactive_sprite
    @staticmethod
    def check_sprite_btn_active(btn,type_btn):
        return UIButtonUtils.check_sprite_state(btn, True, type_btn)
    @staticmethod
    def check_sprite_btn_deactive(btn,type_btn):
        return UIButtonUtils.check_sprite_state(btn, False, type_btn)
class PopupFriend:
    def __init__(self,poco):
        self.poco = poco
        self.root = poco("PopupFriends(Clone)")
        self.title= self.root.offspring("lTitle")
        self.btn_friend = self.root.offspring("B_Friend")
        self.btn_add_friend = self.root.offspring("B_AddFriend")
        self.btn_following= self.root.offspring("B_Following")
        self.btn_back = self.root.offspring("B_Back")
    @property
    def scrollview_friend(self):
        return self.root.offspring("ScrollViewFriends")
    @property
    def scrollview_request(self):
        return self.root.offspring("ScrollViewRequest")
    @property
    def scrollview_follow(self):
        return self.root.offspring("ScrollViewFollowing")
    @property
    def search_panel(self): #group of typing field and search button
        return self.root.offspring("Bot")



