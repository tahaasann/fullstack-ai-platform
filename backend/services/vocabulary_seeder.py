"""Seed English vocabulary, sentence patterns, and work scenarios from JSON files."""
import os
import json
from sqlalchemy.orm import Session
from models import EnglishVocabulary, SentencePattern, WorkScenario
from utils.logger import get_logger

logger = get_logger(__name__)

CONTENT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "content")
ENGLISH_DIR = os.path.join(CONTENT_DIR, "english")


def seed_vocabulary(db: Session):
    """Seed vocabulary from vocabulary.json — idempotent."""
    vocab_path = os.path.join(ENGLISH_DIR, "vocabulary.json")
    if not os.path.exists(vocab_path):
        logger.info("vocabulary.json not found, skipping vocabulary seed")
        return 0

    with open(vocab_path, "r", encoding="utf-8") as f:
        vocab_data = json.load(f)

    count = 0
    for item in vocab_data:
        term = item.get("term", "")
        if not term:
            continue

        existing = db.query(EnglishVocabulary).filter(EnglishVocabulary.term == term).first()
        if existing:
            # Update existing with new fields
            existing.definition_en = item.get("definition_en", "")
            existing.definition_tr = item.get("definition_tr", "")
            existing.difficulty_level = item.get("difficulty_level", "beginner")
            existing.usage_context = item.get("usage_context", "")
            existing.common_patterns = json.dumps(item.get("common_patterns", []), ensure_ascii=False)
            existing.scenario = item.get("scenario", "")
            existing.related_terms = json.dumps(item.get("related_terms", []), ensure_ascii=False)
            existing.common_mistakes = item.get("common_mistakes", "")
            existing.example_sentences = json.dumps(item.get("example_sentences", []), ensure_ascii=False)
            if item.get("pronunciation"):
                existing.pronunciation = item["pronunciation"]
            if item.get("translation"):
                existing.translation = item["translation"]
            if item.get("domain"):
                existing.domain = item["domain"]
            if item.get("lesson_id"):
                existing.lesson_id = item["lesson_id"]
        else:
            vocab = EnglishVocabulary(
                term=term,
                translation=item.get("translation", ""),
                pronunciation=item.get("pronunciation", ""),
                example_sentence=item.get("example_sentences", [{}])[0].get("en", "") if item.get("example_sentences") else "",
                domain=item.get("domain", ""),
                lesson_id=item.get("lesson_id", ""),
                definition_en=item.get("definition_en", ""),
                definition_tr=item.get("definition_tr", ""),
                difficulty_level=item.get("difficulty_level", "beginner"),
                usage_context=item.get("usage_context", ""),
                common_patterns=json.dumps(item.get("common_patterns", []), ensure_ascii=False),
                scenario=item.get("scenario", ""),
                related_terms=json.dumps(item.get("related_terms", []), ensure_ascii=False),
                common_mistakes=item.get("common_mistakes", ""),
                example_sentences=json.dumps(item.get("example_sentences", []), ensure_ascii=False)
            )
            db.add(vocab)
            count += 1

    db.commit()
    logger.info(f"Vocabulary seeded: {count} new terms added")
    return count


def seed_patterns(db: Session):
    """Seed sentence patterns from sentence_patterns.json — idempotent."""
    patterns_path = os.path.join(ENGLISH_DIR, "sentence_patterns.json")
    if not os.path.exists(patterns_path):
        logger.info("sentence_patterns.json not found, skipping patterns seed")
        return 0

    with open(patterns_path, "r", encoding="utf-8") as f:
        patterns_data = json.load(f)

    count = 0
    idx = 0
    for domain_group in patterns_data:
        domain = domain_group.get("domain", "")
        for category_group in domain_group.get("categories", []):
            category = category_group.get("category", "")
            for pattern_item in category_group.get("patterns", []):
                pattern_text = pattern_item.get("pattern", "")
                if not pattern_text:
                    continue

                existing = db.query(SentencePattern).filter(
                    SentencePattern.domain == domain,
                    SentencePattern.pattern == pattern_text
                ).first()

                if not existing:
                    sp = SentencePattern(
                        domain=domain,
                        category=category,
                        pattern=pattern_text,
                        turkish=pattern_item.get("turkish", ""),
                        when_to_use=pattern_item.get("when_to_use", ""),
                        variations=json.dumps(pattern_item.get("variations", []), ensure_ascii=False),
                        real_example=pattern_item.get("real_example", ""),
                        order_index=idx
                    )
                    db.add(sp)
                    count += 1
                idx += 1

    db.commit()
    logger.info(f"Sentence patterns seeded: {count} new patterns added")
    return count


def seed_scenarios(db: Session):
    """Seed work scenarios from scenarios.json — idempotent."""
    scenarios_path = os.path.join(ENGLISH_DIR, "scenarios.json")
    if not os.path.exists(scenarios_path):
        logger.info("scenarios.json not found, skipping scenarios seed")
        return 0

    with open(scenarios_path, "r", encoding="utf-8") as f:
        scenarios_data = json.load(f)

    count = 0
    for i, item in enumerate(scenarios_data):
        sid = item.get("id", f"scenario-{i}")
        existing = db.query(WorkScenario).filter(WorkScenario.id_str == sid).first()

        if not existing:
            scenario = WorkScenario(
                id_str=sid,
                title=item.get("title", ""),
                context=item.get("context", ""),
                dialogue=json.dumps(item.get("dialogue", []), ensure_ascii=False),
                key_phrases=json.dumps(item.get("key_phrases", []), ensure_ascii=False),
                cultural_note=item.get("cultural_note", ""),
                domain=item.get("domain", ""),
                order_index=i
            )
            db.add(scenario)
            count += 1

    db.commit()
    logger.info(f"Work scenarios seeded: {count} new scenarios added")
    return count


def seed_all_english(db: Session):
    """Seed all English content."""
    v = seed_vocabulary(db)
    p = seed_patterns(db)
    s = seed_scenarios(db)
    logger.info(f"English content seeded: {v} vocab, {p} patterns, {s} scenarios")
