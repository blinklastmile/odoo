from odoo.addons.blink.config._env import BLINK_ADMIN_BASE_URL


def get_delivery_url(id=None):
    return "{}admin/database/delivery/?q={}".format(BLINK_ADMIN_BASE_URL, id) if id is not False else None
