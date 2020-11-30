import { extend } from 'vee-validate'
import VueI18n from 'vue-i18n';
import Vue from 'vue';

import {
  required,
  email,
  min,
  confirmed,
  max,
  regex,
  alpha_num,
  alpha,
  alpha_spaces,
  min_value
} from 'vee-validate/dist/rules'

Vue.use(VueI18n)

let locale = localStorage.getItem('locale')
locale = locale ? locale : 'en'

const messages = {
  en: {
    passMin: "Password must be greater than or equal to 8 characters",
    pwdLength: "Password must be greater than or equal to 8 characters and contain only Latin characters",
    required: "This field is required",
    email: "Invalid mail",
    confirmed: "Passwords do not match",
    pwdContain: "The password must only consist of latin characters and numbers",
    pwdLowChar: "Password must contain at least one lowercase character",
    pwdUpChar: "Password must contain at least one uppercase character",
    pwdDigit: "Password must contain at least one digit",
    userLength: `Your username does not match our username standard, make sure: <br>
   - Your name is more than 6 and less than 20 characters. <br>
   - Your name does not contain underscores - neither at the beginning nor at the end. <br>
   - Your name does not contain specials. characters. <br>
   - Your name consists only of latin characters. <br> `,
    userLength2: "Username must contain 6-20 symbols. Disallowed any number, nor special characters. Only Latin letters are allowed.",
    user: "Username cannot contain double underscores, nor can it contain underscores at the beginning or end."
  },
  ru: {
    passMin: "Пароль должен быть больше или равен 8 символам",
    pwdLength: "Пароль должен быть больше или равен 8 символам и содержать только латинские символы",
    required: "Это поле обязательно",
    email: "Не валидная почта",
    confirmed: "Пароли не совпадают",
    pwdContain: "Пароль должен состоять только из символов латинского алфавита и цифр",
    pwdLowChar: "Пароль должен содержать минимум один строчный символ",
    pwdUpChar: "Пароль должен содержать минимум один заглавный символ",
    pwdDigit: "Пароль должен содержать минимум одину цифру",
    userLength: `Ваше имя пользователя не соответствует нашему стандарту имён пользователей, убедитесь что:<br>
  — Ваше имя больше 6 и меньше 20 символов. <br>
  — Ваше имя не содержит нижние подчеркивания — ни в начале, ни в конце. <br>
  — Ваше имя не содержит спец. символов. <br>
  — Ваше имя состоит только из латинских символов. <br>`,
    userLength2: "Имя пользователя должно быть больше или равно 6 и меньше или равно 20 символам и не содержать спец. символов. Допускаются только латинские буквы",
    user: "Имя пользователя не может содержать двойное нижнее подчеркивание, так же не может содержать нижнее подчеркивание в начале или конце"
  }
}

const i18n = new VueI18n({
  locale: locale,
  fallbackLocale: 'en',
  messages
});


extend('email', {
  ...email,
  message: i18n.t('email')
})
extend('min', {
  ...min,
  message: i18n.t('passMin')
})
extend('max', max)
extend('regex', regex)
extend('alpha', alpha)
extend('alpha_num', alpha_num)
extend('alpha_spaces', alpha_spaces)
extend('required', {
  ...required,
  message: i18n.t('required')
})
extend('confirmed', {
  ...confirmed,
  message: i18n.t('confirmed')
})

// PASSWORD EXCEPTIONS
extend('pwdLength', {
  message: i18n.t('pwdLength'),
  validate: value => value.match(/^[a-zA-Z\d]{8,}/) !== null
})
extend('pwdContain', {
  message: i18n.t('pwdContain'),
  validate: value => value.match(/^(?=.*[a-zA-Z\d])/) !== null
})
extend('pwdLowChar', {
  message: i18n.t('pwdLowChar'),
  validate: value => value.match(/^(?=.*[a-z])/) !== null
})
extend('pwdUpChar', {
  message: i18n.t('pwdUpChar'),
  validate: value => value.match(/^(?=.*[A-Z])/) !== null
})
extend('pwdDigit', {
  message: i18n.t('pwdDigit'),
  validate: value => value.match(/^(?=.*\d)/) !== null
})

// USERNAME EXCEPTIONS
extend('userLength', {
  message: i18n.t('userLength'),
  validate: value => value.match(/^(?=[a-zA-Z0-9._]{6,20}$)(?!.*[_.]{2})[^_.].*[^_.]$/) !== null
})
extend('userLength', {
  message: i18n.t('userLength2'),
  validate: value => value.match(/^(?=[a-zA-Z0-9._]{6,20}$)/) !== null
})
extend('user__', {
  message: i18n.t('user'),
  validate: value => value.match(/^(?!.*[_.]{2})[^_.].*[^_.]$/) !== null
})

