// login.page.js
import Page from './page'


class LoginPage extends Page {

  get username() {
    return $('[name=username]')
  }

  get password() {
    return $('[name=password]')
  }

  get submitBtn() {
    return $('[type=submit]')
  }

  get flash() {
    return $('#flash')
  }

  open() {
    //https://verify-core-y5irwcf63a-ew.a.run.app/
    super.open('accounts/login/')
  }

  submit() {
    this.submitBtn.click()
  }

}

export default new LoginPage()