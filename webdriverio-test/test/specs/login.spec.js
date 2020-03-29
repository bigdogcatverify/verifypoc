import LoginPage from '../pageobjects/login.page';
import UserHomePage from '../pageobjects/user-home.page';
import {expect} from 'chai';

describe('Log in', () => {
  it('should allow access', () => {
    LoginPage.open();
    LoginPage.username.setValue('Homer');
    LoginPage.password.setValue('Passw0rd123');
    LoginPage.submit();

    expect(UserHomePage.username.getText()).to.equal('Homer');
  });

  it('should deny access', () => {
    LoginPage.open();
    LoginPage.username.setValue('Someone');
    LoginPage.password.setValue('Not allowed');
    LoginPage.submit();

    expect(LoginPage.flash.getText()).to.contain('Your username and password didn\'t match');
  });
});
