import os
from cudatext import *
from cudax_lib import get_translation

_ = get_translation(__file__) # I18N


class Command:

    def run(self):
        dlg_w = 300
        dlg_h = 600
        padding = 10

        btn_w = int(dlg_w/2-2*padding+padding/2)
        btn_h = 50

        clb_x1 = padding
        clb_x2 = padding
        clb_y1 = int(dlg_w-padding)
        clb_y2 = int(dlg_h-2*padding-btn_h)

        btn_x = padding
        btn_y = int(dlg_h-btn_h-padding)

        btnc_x = int(dlg_w/2+padding/2)
        btnc_y = int(dlg_h-btn_h-padding)

        ign_list = [
            os.path.dirname(os.path.abspath(__file__)).split(os.sep)[-1],
            '__pycache__',
            'sys',
            '__trash'
        ]

        FILE_DISABLED = 'plugin_disabled'

        py_dir = app_path(APP_DIR_PY)
        plugins_list = {}
        for plug in os.listdir(py_dir):
            if os.path.isdir(os.path.join(py_dir, plug)) and plug not in ign_list:
                plugins_list[plug] = '0' if os.path.exists(os.path.join(py_dir, plug, FILE_DISABLED)) else '1'

        c1 = chr(1)
        plugins_list = dict(sorted(plugins_list.items()))
        clb_val = '0;' + ','.join(plugins_list.values())
        res = dlg_custom(_('Plugins'), dlg_w, dlg_h, '\n'.join([]
            + [c1.join(['type=checklistbox', 'items='+'\t'.join(plugins_list), 'val='+clb_val, 'pos=%d,%d,%d,%d'%(clb_x1, clb_x2, clb_y1, clb_y2)])]
            + [c1.join(['type=button', 'cap='+_('&OK'), 'pos=%d,%d'%(btn_x, btn_y), 'w='+str(btn_w), 'h='+str(btn_h)])]
            + [c1.join(['type=button', 'cap='+_('&Cancel'), 'pos=%d,%d'%(btnc_x, btnc_y), 'w='+str(btn_w), 'h='+str(btn_h)])]
        ))
        if res is None: return
        (btn, text) = res
        if btn != 1: return
        items = text.split(';')[1].split(',')

        plugins_list_e = [s for (n, s) in enumerate(plugins_list) if items[n] == '1']

        e_ = []
        d_ = []
        for plug in plugins_list:
            d_path = os.path.join(py_dir, plug, FILE_DISABLED)
            if plug in plugins_list_e:
                if os.path.exists(d_path):
                    os.remove(d_path)
                    e_.append(plug)
            else:
                if not os.path.exists(d_path):
                    open(os.path.join(py_dir, plug, FILE_DISABLED), 'a').close()
                    d_.append(plug)

        msg_ = ''
        if len(e_) > 0:
            msg_ += _('Enabled') + ':\n' + '\n'.join(e_) + '\n\n'
        if len(d_) > 0:
            msg_ += _('Disabled') + ':\n' + '\n'.join(d_) + '\n\n'
        msg_box(msg_ + _('Updates appear after restarting the program.'), MB_OK+MB_ICONINFO)
