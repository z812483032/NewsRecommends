<template>
    <div>
        <wmenu></wmenu>
        <Table :columns="columns10" :data="data9"></Table>
    </div>
</template>
<script>
import expandRow from '../components/table-expand'
import wmenu from '../components/WhiteMenu'

export default {
    // eslint-disable-next-line vue/no-unused-components
    components: { expandRow, wmenu },
    data() {
        return {
            columns10: [
                {
                    type: 'expand',
                    width: 50,
                    render: (h, params) => h(expandRow, {
                        props: {
                            row: params.row,
                        },
                    }),
                },
                {
                    title: '发件人',
                    key: 'sender',
                },
                {
                    title: '主题',
                    key: 'topic',
                },
                {
                    title: '时间',
                    key: 'time',
                },
            ],
            data9: [
                {
                    sender: 'John Brown',
                    age: 18,
                    topic: 'New York No. 1 Lake Park',
                    time: 'Data engineer',
                    interest: 'badminton',
                    birthday: '1991-05-14',
                    book: 'Steve Jobs',
                    movie: 'The Prestige',
                    music: 'I Cry',
                },
                {
                    sender: 'Jim Green',
                    age: 25,
                    topic: 'London No. 1 Lake Park',
                    job: 'Data Scientist',
                    interest: 'volleyball',
                    time: '1989-03-18',
                    book: 'My Struggle',
                    movie: 'Roman Holiday',
                    music: 'My Heart Will Go On',
                },
            ],
        }
    },
}
</script>
