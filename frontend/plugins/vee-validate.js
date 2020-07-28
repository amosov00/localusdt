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
extend('upCase', {
  message: "Пароль должен содержать минимум один заглавный символ",
  validate: value => value.match(/[A-Z]/g) !== null
})
extend('number', {
  message: "Пароль должен содержать минимум одину цифру",
  validate: value => value.match(/[0-9]/g) !== null
})
