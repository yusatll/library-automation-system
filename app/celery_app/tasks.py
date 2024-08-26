from celery import Task
from .celery import celery_app
from app import crud, models
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.dependencies import SessionLocal

# SQLAlchemy oturumu kullanacak görevler için temel sınıf
class SqlAlchemyTask(Task):
    _session = None

    def after_return(self, *args, **kwargs):
        if self._session is not None:
            self._session.close() # Görev bittikten sonra oturumu kapat

    @property
    def session(self) -> Session:
        if self._session is None:
            self._session = SessionLocal() # Gerektiğinde oturum oluştur
        return self._session


# `send_overdue_reminders` görevi, gecikmiş kitap kiralama hatırlatmaları gönderir
@celery_app.task(base=SqlAlchemyTask)
def send_overdue_reminders(self):
    db = self.session
    # Veritabanından gecikmiş kiralamaları getir
    overdue_checkouts = crud.get_overdue_checkouts(db)
    
    for checkout in overdue_checkouts:
        patron = checkout.patron
        book = checkout.book
        days_overdue = (datetime.now() - checkout.due_date).days # Gecikme süresi
        
        # In a real application, you would send an email here
        print(f"Sending reminder to {patron.name} ({patron.email}) for overdue book: "
              f"'{book.title}' by {book.author}. It is {days_overdue} days overdue.")
    
    return f"Sent {len(overdue_checkouts)} overdue reminders."

# `generate_weekly_report` görevi, haftalık rapor oluşturur
@celery_app.task(base=SqlAlchemyTask)
def generate_weekly_report(self):
    db = self.session
    end_date = datetime.now()  # Raporun bitiş tarihi (bugün)
    start_date = end_date - timedelta(days=7) # Raporun başlangıç tarihi (bir hafta önce)
    
    # Veritabanından haftalık kiralama ve iade sayıları getir
    checkouts = crud.get_checkouts_in_period(db, start_date, end_date)
    returns = crud.get_returns_in_period(db, start_date, end_date)
    
    report = f"Weekly Library Report ({start_date.date()} to {end_date.date()}):\n"
    report += f"Total Checkouts: {len(checkouts)}\n"
    report += f"Total Returns: {len(returns)}\n"
        
    # Gerçek uygulamada rapor bir dosyaya kaydedilebilir veya e-posta ile gönderilebilir
    print(report)
    
    return "Weekly report generated successfully."
