from config.models import Menu

def show_menu():
    m_roots = Menu.objects.filter(parent_id=0)
    menu_list=[]
    for m_root in m_roots:
        m_root_list=[{'menu_link':m_root.menu_link,'menu_name':m_root.menu_name}]+[{'menu_link':m.menu_link,'menu_name':m.menu_name} for m in Menu.objects.filter(parent_id=m_root.menuid)]
        menu_list.append(m_root_list)
    return menu_list