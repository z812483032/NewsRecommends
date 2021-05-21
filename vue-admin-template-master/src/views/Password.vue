<template>
    <div style="vertical-align: middle">
        <Form ref="formCustom" :height="tableHeight" :model="formCustom"
              :rules="ruleCustom" :label-width="80" style="width: 500px; margin: 200px auto 0px;">
            <FormItem label="原密码" prop="passwd">
                <Input type="password" v-model="formCustom.passwd" style="width: 400px"></Input>
            </FormItem>
            <FormItem label="新密码" prop="passwdCheck">
                <Input type="password" v-model="formCustom.passwdCheck" style="width: 400px"></Input>
            </FormItem>
            <FormItem>
                <Button type="primary" @click="handleSubmit('formCustom')">确认</Button>
                <Button @click="handleReset('formCustom')" style="margin-left: 8px">重置</Button>
            </FormItem>
        </Form>
    </div>
</template>

<script>
export default {
    name: 'password',
    mounted() {
        window.onresize = () => {
            this.screenHeight = document.body.clientHeight
            this.tableHeight = this.screenHeight - 300
        }
    },
    data() {
        const validatePass = (rule, value, callback) => {
            if (value === '') {
                callback(new Error('Please enter your password'))
            } else {
                if (this.formCustom.passwdCheck !== '') {
                    // 对第二个密码框单独验证
                    this.$refs.formCustom.validateField('passwdCheck')
                }
                callback()
            }
        }
        const validatePassCheck = (rule, value, callback) => {
            if (value === '') {
                callback(new Error('Please enter your password again'))
            } else if (value !== this.formCustom.passwd) {
                callback(new Error('The two input passwords do not match!'))
            } else {
                callback()
            }
        }
        const validateAge = (rule, value, callback) => {
            if (!value) {
                return callback(new Error('Age cannot be empty'))
            }
            // 模拟异步验证效果
            setTimeout(() => {
                if (!Number.isInteger(value)) {
                    callback(new Error('Please enter a numeric value'))
                } else if (value < 18) {
                    callback(new Error('Must be over 18 years of age'))
                } else {
                    callback()
                }
            }, 1000)
        }
        return {
            tableHeight: window.innerHeight - 250,
            screenHeight: document.body.clientHeight,
            formCustom: {
                passwd: '',
                passwdCheck: '',
                age: '',
            },
            ruleCustom: {
                passwd: [
                    { validator: validatePass, trigger: 'blur' },
                ],
                passwdCheck: [
                    { validator: validatePassCheck, trigger: 'blur' },
                ],
                age: [
                    { validator: validateAge, trigger: 'blur' },
                ],
            },
        }
    },
    methods: {
        handleSubmit(name) {
            this.$refs[name].validate((valid) => {
                if (valid) {
                    this.$Message.success('Success!')
                } else {
                    this.$Message.error('Fail!')
                }
            })
        },
        handleReset(name) {
            this.$refs[name].resetFields()
        },
    },
}
</script>

<style scoped>
.view-c{
    vertical-align: middle;
}

</style>
