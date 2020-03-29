export default class Page {

  login() {
    this.open('accounts/login');
    $('[name=username]').setValue('Homer');
    $('[name=password]').setValue('Passw0rd123');
    $('[type=submit]').click();
  }

  constructor() {
    this.title = 'Verify cats'
  }

  open(path) {
    browser.url(path)
  }
}