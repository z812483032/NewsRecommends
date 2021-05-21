<template>
    <div>
        <Menu mode="horizontal" :theme="theme1" active-name="1">
            <MenuItem name="1">
                <Icon type="ios-paper" />
                全部消息
            </MenuItem>
            <MenuItem name="2">
                <Icon type="ios-people" />
                未读消息
            </MenuItem>
            <Submenu name="3">
                <template slot="title">
                    <Icon type="ios-stats" />
                    已读消息
                </template>
                <MenuGroup title="使用">
                    <MenuItem name="3-1">新增和启动</MenuItem>
                    <MenuItem name="3-2">活跃分析</MenuItem>
                    <MenuItem name="3-3">时段分析</MenuItem>
                </MenuGroup>
                <MenuGroup title="留存">
                    <MenuItem name="3-4">用户留存</MenuItem>
                    <MenuItem name="3-5">流失用户</MenuItem>
                </MenuGroup>
            </Submenu>
            <MenuItem name="4">
                <Icon type="ios-construct" />
                消息设置
            </MenuItem>
        </Menu>
    </div>
</template>
<script>
export default {
    data() {
        return {
            theme1: 'light',
        }
    },
}
</script>
