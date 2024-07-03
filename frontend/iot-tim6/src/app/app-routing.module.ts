import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { DevicesComponent } from './devices/devices.component';
import { AlarmsComponent } from './alarms/alarms.component';
import { TimersComponent } from './timers/timers.component';
import { ManageComponent } from './manage/manage.component';

const routes: Routes = [
  { path: 'devices', component: DevicesComponent },
  { path: 'alarms', component: AlarmsComponent },
  { path: 'timers', component: TimersComponent },
  { path: 'manage', component: ManageComponent },
  { path: '', redirectTo: '/devices', pathMatch: 'full' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
