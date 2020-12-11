export const state = () => ({
    invoices:null,
    users:null,
})

export const getters = {
    getInvoices(state){
        return state.invoices
    },
    getUsers(state){
        return state.users
    }
}

export const mutations = {
    getInvoices(state, payload){
        state.invoices = payload
    },
    getUsers(state, payload){
        state.users = payload
    },
    editStatus(state, payload){
        state.invoices.forEach(e=>{
            if(e._id == payload.id){
                e.status = payload.status
            }
        })
    }
}

export const actions = {
    async getInvoices({commit}){
        let result =  await this.$axios.get(`/admin/invoices/`)
        commit('getInvoices', result.data)
    },
    async getUsers({commit}){
        let result =  await this.$axios.get(`/admin/users/`)
        commit('getUsers', result.data)
    },
    async userStatus(state, payload){
        let url;
        if(payload.value == 1){
            url = `/admin/users/status/${payload.user}/active`
        }
        if(payload.value == 2){
            url = `/admin/users/status/${payload.user}/freezed`
        }
        if(payload.value == 3){
            url = `/admin/users/status/${payload.user}/blocked`
        }
        await this.$axios.put(url)
    },
    async editStatus({commit}, payload){
        commit('editStatus', payload)
    }
}
