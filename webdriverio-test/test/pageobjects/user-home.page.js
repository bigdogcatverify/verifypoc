import Page from './page'

class LoginPage extends Page {

  get username() {
    return $('#username')
  }

  open() {
    super.open('')
  }

}

export default new LoginPage()