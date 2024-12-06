页面：功能 -> 相应跳转页面



Index: 欢迎页面 -> login, register

login: 登录页面 -> Index, person

register: 注册页面 -> Index

(登录之后可以给不同身份的人做不同页面，根据role，放不同的功能按钮上去)

person_staff: person主页面 -> find_item, find_order, accept_donation, start_order, shopping, prepare_order, relevant_order

person_client: person主页面 -> find_item, find_order, relevant_order

person_donor: person主页面 -> find_item, find_order, relevant_order

person_volunteer: person主页面 -> find_item, find_order, prepare_order, relevant_order

我发现还是合在一起做，虽然理论上客户和管理员登录进去应该是不一样的页面，但那样太麻烦了，要重写好多方法

person: 主页面 -> find_item, find_order, accept_donation, start_order, shopping, prepare_order, relevant_order



find_item: 按ID找一个物品，并列出其组件位置 -> person

find_order: 按ID找订单，并列出所有物品的位置 -> person

accept_donation: 以staff身份接受donor捐赠，接收一个物品及所有组件的位置 -> person



我们要做duplicate items吗？(feature12)

start_order: 以staff身份添加order -> person_staff

shopping: 以staff身份添加item到现有order -> shopping, person_staff

prepare_order: 以volunteer或staff身份修改order中item的状态 -> person_staff, person_volunteer

relevant_order: 显示所有和当前账号相关的order -> person

