import { extend, localize } from 'vee-validate'
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
import en from 'vee-validate/dist/locale/en.json'

localize({
  en
})

extend('email', {
  ...email,
  message: 'Не валидная почта'
})
extend('min', {
  ...min,
  message: 'Пароль должен быть больше или равен 8 символам'
})
extend('max', max)
extend('regex', regex)
extend('alpha', alpha)
extend('alpha_num', alpha_num)
extend('alpha_spaces', alpha_spaces)
extend('required', {
  ...required,
  message: 'Это поле обязательно'
})
extend('confirmed', {
  ...confirmed,
  message: 'Пароли не совпадают'
})

// PASSWORD EXCEPTIONS
extend('pwdLength', {
  message: 'Пароль должен быть больше или равен 8 символам и содержать только латинские символы',
  validate: value => value.match(/^[a-zA-Z\d]{8,}/) !== null
})
extend('pwdContain', {
  message: 'Пароль должен состоять только из символов латинского алфавита и цифр',
  validate: value => value.match(/^(?=.*[a-zA-Z\d])/) !== null
})
extend('pwdLowChar', {
  message: 'Пароль должен содержать минимум один строчный символ',
  validate: value => value.match(/^(?=.*[a-z])/) !== null
})
extend('pwdUpChar', {
  message: 'Пароль должен содержать минимум один заглавный символ',
  validate: value => value.match(/^(?=.*[A-Z])/) !== null
})
extend('pwdDigit', {
  message: 'Пароль должен содержать минимум одину цифру',
  validate: value => value.match(/^(?=.*\d)/) !== null
})

// USERNAME EXCEPTIONS
extend('userLength', {
  message: `Ваше имя пользователя не соответствует нашему стандарту имён пользователей, убедитесь что:<br>
  — Ваше имя больше 6 и меньше 20 символов. <br>
  — Ваше имя не содержит нижние подчеркивания — ни в начале, ни в конце. <br>
  — Ваше имя не содержит спец. символов. <br>
  — Ваше имя состоит только из латинских символов. <br>`,
  validate: value => value.match(/^(?=[a-zA-Z0-9._]{6,20}$)(?!.*[_.]{2})[^_.].*[^_.]$/) !== null
})
extend('userLength', {
  message: 'Имя пользователя должно быть больше или равно 6 и меньше или равно 20 символам и не содержать спец. символов',
  validate: value => value.match(/^(?=[a-zA-Z0-9._]{6,20}$)/) !== null
})
extend('user__', {
  message: 'Имя пользователя не может содержать двойное нижнее подчеркивание, так же не может содержать нижнее подчеркивание в начале или конце',
  validate: value => value.match(/^(?!.*[_.]{2})[^_.].*[^_.]$/) !== null
})

