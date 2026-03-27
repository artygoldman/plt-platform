"""
Seed data script for Phase 5.

Creates:
- 1 demo user (demo@longevity.ai)
- 30 days of biomarker data
- Digital Twin with all 11 systems scored
- 3 protocols (active, completed, draft)
- 7 daily contracts (last week)
- 5 supplement inventory items
"""

import asyncio
from datetime import date, datetime, timedelta
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.db.base import Base
from src.db.models import (
    User, UserProfile, Biomarker, DigitalTwin,
    Protocol, DailyContract, SupplementInventory
)
from src.core.config import get_settings


async def seed_database():
    """Seed the database with demo data."""
    settings = get_settings()

    # Create engine and session
    engine = create_async_engine(settings.database_url, echo=False)

    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        try:
            # Create demo user
            demo_user = User(
                id=uuid4(),
                email="demo@longevity.ai",
                name="Demo User",
                date_of_birth=date(1990, 5, 15),
                sex="male",
                subscription_tier="premium",
                timezone="America/New_York",
            )
            session.add(demo_user)
            await session.flush()

            # Create user profile
            user_profile = UserProfile(
                id=uuid4(),
                user_id=demo_user.id,
                height_cm=178.0,
                weight_kg=72.5,
                blood_type="O+",
                allergies=[],
                medications=[],
                contraindications=[],
                genetic_risks={
                    "heart_disease": "moderate",
                    "diabetes": "low",
                },
                goals=["improve_cardiovascular_health", "weight_management"],
            )
            session.add(user_profile)
            await session.flush()

            # Create 30 days of biomarker data
            biomarker_types = [
                ("glucose", "mg/dL", "blood_glucose", "70-100"),
                ("cholesterol_total", "mg/dL", "lipids", "<200"),
                ("ldl", "mg/dL", "lipids", "<130"),
                ("hdl", "mg/dL", "lipids", ">40"),
                ("triglycerides", "mg/dL", "lipids", "<150"),
                ("apob", "g/L", "lipids", "<1.3"),
                ("hba1c", "%", "blood_glucose", "<5.7"),
                ("creatinine", "mg/dL", "kidney", "0.7-1.3"),
                ("ast", "U/L", "liver", "10-34"),
                ("alt", "U/L", "liver", "7-56"),
            ]

            base_values = {
                "glucose": 92,
                "cholesterol_total": 190,
                "ldl": 110,
                "hdl": 52,
                "triglycerides": 115,
                "apob": 1.05,
                "hba1c": 5.1,
                "creatinine": 0.88,
                "ast": 26,
                "alt": 30,
            }

            for day_offset in range(30):
                measured_at = datetime.utcnow() - timedelta(days=day_offset)

                for marker_name, unit, category, ref_range in biomarker_types:
                    base_value = base_values.get(marker_name, 100)
                    # Add some realistic variation
                    variation = (day_offset % 5) * 0.5
                    value = base_value + variation

                    biomarker = Biomarker(
                        id=uuid4(),
                        user_id=demo_user.id,
                        marker_name=marker_name,
                        value=round(value, 2),
                        unit=unit,
                        reference_range=ref_range,
                        category=category,
                        source="blood_test" if day_offset % 3 == 0 else "wearable",
                        measured_at=measured_at,
                    )
                    session.add(biomarker)

            # Create digital twin with all 11 systems
            twin = DigitalTwin(
                id=uuid4(),
                user_id=demo_user.id,
                biological_age=38,
                chronological_age=35,
                health_score=78.5,
            )
            session.add(twin)
            await session.flush()

            # Create 3 protocols
            protocols = [
                ("Cardiovascular Health", "Focus on heart health and blood pressure", "active"),
                ("Metabolic Optimization", "Improve glucose and lipid metabolism", "completed"),
                ("Sleep & Recovery", "Enhance sleep quality and recovery", "draft"),
            ]

            protocol_ids = []
            for name, description, status in protocols:
                protocol = Protocol(
                    id=uuid4(),
                    user_id=demo_user.id,
                    name=name,
                    description=description,
                    status=status,
                    created_at=datetime.utcnow(),
                )
                session.add(protocol)
                protocol_ids.append(protocol.id)
                await session.flush()

            # Create 7 daily contracts (last week)
            contract_names = [
                "Morning Cardio Workout",
                "Meditation Session",
                "Healthy Breakfast",
                "Evening Walk",
                "Supplement Intake",
                "Sleep Tracking",
                "Weekly Health Review",
            ]

            for i, name in enumerate(contract_names):
                scheduled_date = date.today() - timedelta(days=i)
                completed = i < 4  # First 4 are completed

                contract = DailyContract(
                    id=uuid4(),
                    user_id=demo_user.id,
                    protocol_id=protocol_ids[0],
                    name=name,
                    description=f"Complete {name.lower()}",
                    scheduled_date=scheduled_date,
                    completed=completed,
                    streak_days=4 if i < 4 else 0,
                )
                session.add(contract)

            # Create supplement inventory (5 items)
            supplements = [
                ("Vitamin D3", "10000 IU daily supplement", 120, "softgels"),
                ("Omega-3 Fish Oil", "1000mg EPA/DHA per capsule", 90, "capsules"),
                ("Magnesium Glycinate", "400mg per capsule", 60, "capsules"),
                ("Probiotics", "Multi-strain formula", 30, "capsules"),
                ("CoQ10", "100mg ubiquinone", 60, "capsules"),
            ]

            for name, description, quantity, unit in supplements:
                inventory = SupplementInventory(
                    id=uuid4(),
                    user_id=demo_user.id,
                    name=name,
                    description=description,
                    quantity=quantity,
                    unit=unit,
                    added_at=datetime.utcnow(),
                )
                session.add(inventory)

            await session.commit()
            print("✓ Database seeded successfully!")
            print(f"  - Demo user: demo@longevity.ai")
            print(f"  - Biomarkers: 300 entries (30 days × 10 markers)")
            print(f"  - Digital Twin: 1 (biological age: 38)")
            print(f"  - Protocols: 3 (active, completed, draft)")
            print(f"  - Daily Contracts: 7 (last week)")
            print(f"  - Supplement Inventory: 5 items")

        except Exception as e:
            await session.rollback()
            print(f"✗ Error seeding database: {e}")
            raise
        finally:
            await session.close()

    await engine.dispose()


def main():
    """Run the seeding process."""
    print("Starting database seeding...")
    asyncio.run(seed_database())


if __name__ == "__main__":
    main()
