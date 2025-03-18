import time
from sqlalchemy import TIMESTAMP, Boolean, Column, Float, ForeignKey, ForeignKeyConstraint, Integer, String, text, create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import schedule

Base = declarative_base()


class Users(Base):
    __tablename__ = "users"

    user_email = Column(String, primary_key=True, nullable=False)
    cf_handle = Column(String, unique=True, nullable=False, index=True)
    user_name = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)  # Changed to password_hash
    year = Column(String, nullable=False)
    cf_rating = Column(Integer, server_default='0', index=True)


class Rating(Base):
    __tablename__ = "ratings"

    cf_handle = Column(String, primary_key=True)
    total_rating = Column(Integer, server_default='0', index=True)


class Contests(Base):
    __tablename__ = "contests"
    contest_id = Column(Integer, primary_key=True, autoincrement=True)
    contest_name = Column(String, nullable=False, unique=True)


class ContestTable(Base):
    # This will be dynamically created
    __tablename__ = "contest_table_{contest_id}"

    name = Column(String, nullable=True)
    cf_handle = Column(String, nullable=False, primary_key=True)
    number_of_solved_problems = Column(Integer, default=0)
    contest_rank = Column(Integer, nullable=False)


class WeeklyLeaderBoard(Base):
    __tablename__ = "weeklyleaderboard"

    user_email = Column(String, primary_key=True, nullable=False)
    cf_handle = Column(String, nullable=False)
    real_name = Column(String, nullable=True)
    number_of_solved_problems = Column(Integer, default=0, index=True)

    @classmethod
    def reset_weekly_solved_problems(cls, session):
        """Resets the number of solved problems to 0 for all users."""
        session.query(cls).update({cls.number_of_solved_problems: 0})
        session.commit()

    @classmethod
    def schedule_weekly_reset(cls, session):
        """Schedules the weekly reset of solved problems."""
        def weekly_reset():
            cls.reset_weekly_solved_problems(session)

        # Schedule the job to run every week at a specific time
        schedule.every().week.do(weekly_reset)

        # Keep the scheduler running
        # while True:
        #     schedule.run_pending()
        #     time.sleep(1)

# Dynamic table creation for contests


@event.listens_for(Contests, 'after_insert')
def create_contest_table(mapper, connection, target):
    contest_table = type(f'ContestTable_{target.contest_id}', (Base,), {
        '__tablename__': f'contest_table_{target.contest_id}',
        'name': Column(String, nullable=True),
        'cf_handle': Column(String, primary_key=True),
        'number_of_solved_problems': Column(Integer, default=0),
        'contest_rank': Column(Integer, nullable=False)
    })
    contest_table.__table__.create(connection)
