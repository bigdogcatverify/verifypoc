import {expect} from 'chai';
import UserEventsPage from "../pageobjects/user-events.page";
import addEventPageFactory from "../pageobjects/add-event-factory.page";
const AddAddressEventPage = addEventPageFactory('address');

describe('Events', () => {
  before(() => UserEventsPage.login());

  it('Should show address event', () => {
    UserEventsPage.open();
    expect(UserEventsPage.addressHistory.getText()).to.contain('742 Evergreen Terrace');
  });

  it('Should add an address', () => {
    UserEventsPage.open();
    UserEventsPage.addLivingEvent();

    expect(AddAddressEventPage.eventDetailInputLabel.getText()).to.equal('Address:');

    AddAddressEventPage.startDate.setValue('15/01/2004');
    AddAddressEventPage.endDate.setValue('13/03/2009');
    AddAddressEventPage.eventDetailInputLabel.setValue('105 Something Place, cool ville');
    AddAddressEventPage.verifier.selectByAttribute('value', '1');
    AddAddressEventPage.submit();

    // todo should navigate back to events page
    UserEventsPage.open();
    expect(UserEventsPage.addressHistory.getText()).to.contain('105 Something Place, cool ville')
  });
});
