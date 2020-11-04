<template lang="pug">
  div
    //--div
      button(@click="notify") Notify
    div.notify-center
      //--span(style="position: absolute; font-size: 13px;") {{ connected ? '+' : '' }}
      div.notify-center__icon(@click.stop="toggle" :class="{ 'notify-center__icon--active': showMessages}")
        InlineSvg(:src="require('~/assets/icons/notification.svg')")
        div.notify-center__badge(v-show="showBadge")
      transition(name="fade")
        div.notify-center__popup(v-if="showMessages" @click.stop)
          div.notify-center__header
            div.notify-center__header-left
              span.notify-center__title {{ $t('other.notifications') }}
              div.notify-center__refresh(@click="loadNotifictions")
                InlineSvg(:src="require('~/assets/icons/refresh.svg')")
            div.notify-center__watch-all(@click="markAllRead") {{ $t('other.mark') }}
          div.notify-center__list(@click="hide")
            div(v-if="notif_list.length === 0").notify-center__empty {{ $t('other.orderNotes') }}
            //--n-link(:to="'/invoice/' + msg.invoice_id" v-for="(msg, i) in notif_list" :class="{ 'status-new' : !msg.watched}" :key="i").notify-center__msg
            div(v-for="(msg, i) in notif_list" :class="{ 'status-new' : !msg.watched}" :key="i").notify-center__msg
              div(v-if="msg.amount")
                div.notify-center__msg-title
                  span(v-if="msg.type === 2") {{ $t('other.replenishment') }}
                  span(v-if="msg.type === 3") {{ $t('other.withdraw') }}
                  span.notify-center__amount(:class="{ 'notify-center__amount': msg.new_status === 1 }") {{ Number(msg.amount).toFixed(2) }} USDT
                  span(v-if="msg.new_status")
                    = ': '
                  span.color-green {{ msg.new_status }}
                div.notify-center__msg-body
                  div.notify-center__msg-content {{ msg.invoice_id }}
                  div.notify-center__msg-time {{ formatDate(msg.created_at) }}
              div(v-else)
                div.notify-center__msg-title
                  span {{ $t('other.order') }}
                  span(v-if="msg.new_status")
                    = ': '
                  span.color-green {{ msg.new_status }}
                div.notify-center__msg-body
                  div.notify-center__msg-content {{ msg.invoice_id }}
                  div.notify-center__msg-time {{ formatDate(msg.created_at) }}
</template>

<script>
  import InlineSvg from 'vue-inline-svg';

  import formatDate from "~/mixins/formatDate";
  import formatCurrency from "~/mixins/formatCurrency";

  export default {
    components: {InlineSvg},
    mixins: [formatDate, formatCurrency],
    data: () => ({
      connected: false,
      showMessages: false,
      notif_list: [],
      ws: null,
      audio: null
    }),
    mounted() {
      this.loadNotifictions();

      document.body.addEventListener('click', this.hide, false)

      this.ws = new WebSocket(`${process.env.API_WS_URL}notification/ws/`);
      this.ws.onopen = (e) => {
        this.connected = true
      }
      this.ws.onerror = (e) => {
        this.connected = false
      }
      this.ws.onmessage = (e) => {
        const data = JSON.parse(e.data);
        this.notif_list.unshift(data);
        this.notify(data)
      }
    },

    beforeDestroy() {
      document.body.removeEventListener('click', this.hide)
    },

    computed: {
      showBadge() {
        return this.notif_list.findIndex(el => el.watched === false) !== -1;
      }
    },

    methods: {
      async markAllRead() {
        this.$axios.get('/notification/watch/')
          .then(async () => {
            await this.loadNotifictions();
          }).catch(() => {
          })
      },

      async loadNotifictions() {
        this.$axios.get('/notification/')
          .then(res => {
            this.notif_list = res.data;
          }).catch(() => {
          this.$toast.showMessage({content: this.$t('other.notesError'), red: true})
        })
      },

      toggle() {
        this.showMessages = !this.showMessages;
      },

      hide() {
        this.showMessages = false
      },

      notify(data) {
        const title = data.new_status
        const text = `${data.invoice_id}<div class="time">${this.formatDate(data.created_at)}</div>`

        this.$notify({
          group: 'app',
          title,
          text,
          duration: 60000,
          closeOnClick: true,
          speed: 200,
          data: {
            invoice_id: data.invoice_id
          }
        });
        this.playSound('notification-1.mp3')
      },
      playSound(filename) {
        if (this.audio instanceof Audio) {
          this.audio.pause()
          this.audio.currentTime = 0;
        }

        this.audio = new Audio(require(`~/assets/sounds/${filename}`));
        this.audio.play()
      },
    }
  }
</script>

<style lang="scss" scoped>
.color-green {
  color: #48B190;
}

.status-new {
  &:after {
    content: '';
    top: 50%;
    right: 20px;
    width: 10px;
    height: 10px;
    position: absolute;
    background-color: #ED9F43;
    border-radius: 99px;
    transform: translateY(-50%);
  }
}

.fade-enter-active, .fade-leave-active {
  opacity: 1;
  transition: all .2s;
}
.fade-enter, .fade-leave-to {
  opacity: 0;
  transform: translateY(20px);
}

.notify-center {
  position: relative;

  &__badge {
    position: absolute;
    background-color: #ED9F43;
    width: 10px;
    height: 10px;
    border-radius: 99px;
    top: 8px;
    right: 8px;
  }

  &__amount {
    margin-left: 10px;
    font-size: 13px;
    color: #ED9F43;

    &--done {
      color: #48AF8F;
    }
  }

  &__icon {
    width: 40px;
    height: 40px;
    opacity: 1;
    cursor: pointer;
    padding: 3px 10px;
    color: #262626;

    > svg {
      width: 100%;
      height: 100%;
    }

    &:hover {
      background-color: #f1f1f1;
      border-radius: 3px;
    }

    &--active {
      background-color: #f6f6f6;
    }
  }

  &__refresh {
    width: 20px;
    height: 20px;
    display: inline-block;
    margin-left: 10px;
    cursor: pointer;

    &:hover {
      opacity: 0.8;
    }

    svg {
      width: 100%;
    }
  }

  &__header-left {
    display: flex;
    align-items: center;
  }

  &__header {
    padding: 15px 20px;
    border-bottom: 1px solid #cccccc;
    user-select: none;
    background-color: #f8f8f8;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  &__title {
    font-size: 14px;
    font-weight: 500;
  }

  &__watch-all {
    font-size: 13px;
    color: #888888;

    &:hover {
      cursor: pointer;
      color: #5d5d5d;
    }
  }

  &__empty {
    display: flex;
    align-items: center;
    justify-content: center;
    height: calc(100% - 20px);
    text-align: center;
    opacity: 0.4;
    font-size: 14px;
  }

  &__msg {
    display: block;
    padding: 15px 20px;
    border-bottom: 1px solid #cccccc;
    position: relative;
    transition: background-color 200ms;
    background-color: #ffffff;

    &:hover {
      background-color: #fafafa;
      cursor: pointer;
    }

    &-title {
      text-transform: capitalize;
      font-weight: 500;
      margin-bottom: 5px;
    }

    &-time {
      color: #a2a2a2;
      font-size: 12px;
      margin-top: 5px;
    }
  }

  &__list {
    height: 300px;
    overflow-y: scroll;
    &::-webkit-scrollbar {
      width: 10px;
    }

    &::-webkit-scrollbar-track {
      background: #F8F8F8;
    }

    &::-webkit-scrollbar-thumb {
      background: #bfbfbf;
    }

    &::-webkit-scrollbar-thumb:hover {
      background: #9d9d9d;
    }
  }

  &__popup {
    border: 1px solid #cccccc;
    border-radius: 5px;
    left: -320px;
    width: 400px;
    top: 50px;
    z-index: 20000;
    position: absolute;
    background-color: #ffffff;
    box-shadow: 0 8px 9px rgba(67, 78, 74, 0.07), 0 16px 23px rgba(67, 78, 74, 0.09);
    &:before {
      top: -10px;
      right: 50px;
      position: absolute;
      content: '';
      width: 0;
      height: 0;
      border-left: 10px solid transparent;
      border-right: 10px solid transparent;
      border-bottom: 10px solid #cccccc;
    }

    &:after {
      top: -9px;
      right: 51px;
      position: absolute;
      content: '';
      width: 0;
      height: 0;
      border-left: 9px solid transparent;
      border-right: 9px solid transparent;

      border-bottom: 10px solid #ffffff;
    }
  }
}
</style>
