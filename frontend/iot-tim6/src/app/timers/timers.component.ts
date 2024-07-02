// timers.component.ts

import { Component } from '@angular/core';
import { CommsService } from '../comms.service';

@Component({
  selector: 'app-timers',
  templateUrl: './timers.component.html',
  styleUrls: ['./timers.component.css']
})
export class TimersComponent {
  isTimerOn: boolean = true;
  selectedTimeString: string = ''; 

  constructor(private commsService: CommsService) { }

  ngOnInit(): void {
    this.loadTimerState();
  }

  setTimerState(state:boolean): void {
    this.isTimerOn = state;
    localStorage.setItem('timerState', JSON.stringify(state));
  }

  turnOffTimer(): void {
      this.commsService.turnOffTimer();
      this.setTimerState(false);
  }

  private loadTimerState(): void {
    const storedTimerState = localStorage.getItem('timerState');
    if (storedTimerState) {
      this.isTimerOn = JSON.parse(storedTimerState);
    }
  }

  setTimer(): void {
    const currentTime = new Date();
    console.log("balagassssss")
    if (this.isTimerOn==false) {
      console.log("balagas")
      if (this.selectedTimeString) {
        const [hours, minutes] = this.selectedTimeString.split(':');
        const selectedDateTime = new Date(currentTime.getFullYear(), currentTime.getMonth(), currentTime.getDate(), parseInt(hours), parseInt(minutes));

        console.log(selectedDateTime);
        console.log(currentTime);

        const oneMinuteAhead = new Date(currentTime);
        oneMinuteAhead.setMinutes(oneMinuteAhead.getMinutes() + 1);

        if (selectedDateTime > oneMinuteAhead) {
          console.log('Setting timer for:', selectedDateTime);
          alert("Timer is set")
          this.setTimerState(true)
          this.commsService.sendTimer(selectedDateTime);
        } else {
          alert('Invalid timer value. Please select a time at least one minute in the future.');
        }

        return
      } 
      else 
      {
        alert('Please select a valid time');
      }
    }
  }


}
