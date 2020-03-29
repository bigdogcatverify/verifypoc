import Page from './page'

class UserEventsPage extends Page {

  get addressHistory() {
    return $('#address-history')
  }

  get addLivingEventLink() {
    return $('#add-living-event');
  }

  open() {
    super.open('events')
  }

  addLivingEvent() {
    this.addLivingEventLink.click()
  }
}

export default new UserEventsPage()