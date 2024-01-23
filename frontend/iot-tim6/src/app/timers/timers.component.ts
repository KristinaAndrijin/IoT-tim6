// timers.component.ts

import { Component } from '@angular/core';

@Component({
  selector: 'app-timers',
  templateUrl: './timers.component.html',
  styleUrls: ['./timers.component.css']
})
export class TimersComponent {
  isTimerOn: boolean = true;
  selectedTimeString: string = ''; 

  constructor() { }

  toggleTimer(): void {
    this.isTimerOn = !this.isTimerOn;
  }

  setTimer(): void {
    const currentTime = new Date();
    
    if (this.selectedTimeString) {
      const [hours, minutes] = this.selectedTimeString.split(':');
      const selectedDateTime = new Date(currentTime.getFullYear(), currentTime.getMonth(), currentTime.getDate(), parseInt(hours), parseInt(minutes));

      console.log(selectedDateTime);
      console.log(currentTime);

      const oneMinuteAhead = new Date(currentTime);
      oneMinuteAhead.setMinutes(oneMinuteAhead.getMinutes() + 1);

      if (selectedDateTime > oneMinuteAhead) {
        console.log('Setting timer for:', selectedDateTime);
      } else {
        console.error('Invalid timer value. Please select a time at least one minute in the future.');
      }
    } else {
      console.error('Please select a valid time');
    }
  }
}
