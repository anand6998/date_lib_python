from abc import ABCMeta, abstractmethod
from datetime import datetime
from typing import List, Set, Dict

fmt: str = '%Y-%m-%d'


class IWeekendDate(metaclass=ABCMeta):
    @abstractmethod
    def is_weekend_date(self, dt: datetime) -> bool:
        raise NotImplementedError


class USWeekendDate(IWeekendDate):
    def is_weekend_date(self, dt: datetime) -> bool:
        week_no: int = dt.weekday()
        return False if week_no < 5 else True


class IBusinessCalendar:
    @abstractmethod
    def is_business_day(self, dt: datetime) -> bool:
        raise NotImplementedError


class BusinessCalendar(IBusinessCalendar):

    def __init__(self, holidays: List[datetime]):
        self.holidays: List[datetime] = holidays

    def is_business_day(self, dt: datetime) -> bool:
        return True if dt not in self.holidays else False


class CombinedBusinessCalendar(BusinessCalendar):
    def __init__(self, calendars: List[BusinessCalendar] = list()):
        self.calendars: List[BusinessCalendar] = calendars
        holiday_set: Set[datetime] = set()
        for calendar in calendars:
            holiday_set.update(calendar.holidays)

        self.holidays: List[datetime] = list(holiday_set)


weekend_impl_dict: Dict[str, IWeekendDate] = dict()
weekend_impl_dict['US'] = USWeekendDate()


def get_weekend_impl(region: str) -> IWeekendDate:
    return weekend_impl_dict.get(region, None)


class NYSEBusinessCalendar(BusinessCalendar):
    def __init__(self):
        self.holidays = [
            # 2021
            datetime.strptime('2021-01-01', fmt),
            datetime.strptime('2021-01-18', fmt),
            datetime.strptime('2021-02-15', fmt),
            datetime.strptime('2021-04-02', fmt),
            datetime.strptime('2021-05-31', fmt),
            datetime.strptime('2021-07-05', fmt),
            datetime.strptime('2021-09-06', fmt),
            datetime.strptime('2021-11-25', fmt),
            datetime.strptime('2021-12-25', fmt),

            # 2022
            datetime.strptime('2021-01-17', fmt),
            datetime.strptime('2021-02-21', fmt),
            datetime.strptime('2021-04-15', fmt),
            datetime.strptime('2021-05-30', fmt),
            datetime.strptime('2021-07-04', fmt),
            datetime.strptime('2021-09-05', fmt),
            datetime.strptime('2021-11-24', fmt),
            datetime.strptime('2021-12-25', fmt),

            # 2023
            datetime.strptime('2021-01-01', fmt),
            datetime.strptime('2021-01-15', fmt),
            datetime.strptime('2021-02-19', fmt),
            datetime.strptime('2021-03-29', fmt),
            datetime.strptime('2021-05-27', fmt),
            datetime.strptime('2021-06-19', fmt),
            datetime.strptime('2021-07-04', fmt),
            datetime.strptime('2021-09-02', fmt),
            datetime.strptime('2021-11-28', fmt),
            datetime.strptime('2021-12-25', fmt),

        ]


business_calendar_impl: Dict[str, IBusinessCalendar] = dict()
business_calendar_impl['NYSE'] = NYSEBusinessCalendar()


def get_business_calendar(calendar_name: str) -> IBusinessCalendar:
    return business_calendar_impl.get(calendar_name, None)


def is_weekend_dt(dt, region: str = 'US') -> bool:
    weekend_date_impl: IWeekendDate = get_weekend_impl(region=region)
    return weekend_date_impl.is_weekend_date(dt=dt)


def is_calendar_business_dt(dt, calendar_name: str = 'NYSE') -> bool:
    calendar_date_impl: IBusinessCalendar = get_business_calendar(calendar_name=calendar_name)
    return calendar_date_impl.is_business_day(dt=dt)

def is_business_day_nyse(dt: datetime, region: str = 'US', calendar_name: str = 'NYSE') -> bool:
    if not is_weekend_dt(dt=dt, region=region) and is_calendar_business_dt(dt=dt, calendar_name=calendar_name):
        return True
    return False

if __name__ == '__main__':
    region: str = 'US'
    calendar_name: str = 'NYSE'
    dts: List[datetime] = [
        datetime.strptime('2023-01-01', fmt),
        datetime.strptime('2023-07-04', fmt),
        datetime.strptime('2023-06-05', fmt),
        datetime.strptime('2023-05-12', fmt),
        datetime.strptime('2023-05-13', fmt),
        datetime.strptime('2023-05-14', fmt),
    ]

    for dt in dts:
        print(dt, is_business_day_nyse(dt))