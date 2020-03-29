import Page from './page'

class AddEventPage extends Page {

  constructor(eventType) {
    super();
    this.eventType = eventType;
  }


  get startDate() {
    return $('#id_start_date')
  }

  get endDate() {
    return $('#id_end_date');
  }

  get eventDetailInput() {
    return $(`#id_${this.eventType}`);
  }

  get verifier() {
    return $(`#id_verifier`)
  }

  get eventDetailInputLabel() {
    return $(`[for="id_${this.eventType}"]`)
  }

  get verifier() {
    return $('#id_verifier');
  }

  get submitBtn() {
    return $('[type=submit]')
  }

  open() {
    super.open('events')
  }

  submit() {
    this.submitBtn.click()
  }
}

export default (eventType) => new AddEventPage(eventType);