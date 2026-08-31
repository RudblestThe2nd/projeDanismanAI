SKILL_KEYWORDS = {
    "project_idea_refinement": ["proje fikri", "sıfırdan", "ne yapayım", "fikir", "öneri"],
    "report_section_writer": ["problem tanımı", "yöntem yaz", "rapor", "bölüm", "giriş yaz"],
    "tubitak_application_guidance": ["tübitak", "akademik", "başvuru", "araştırma"],
    "teknofest_ktr_ptr_guidance": ["teknofest", "ktr", "ptr", "sistem mimarisi", "teknik rapor"],
    "feasibility_and_risk_check": ["yapılabilir mi", "risk", "uygulanabilir", "maliyet"],
    "title_abstract_generator": ["başlık", "özet", "abstract", "title"],
    "presentation_and_jury_preparation": ["sunum", "jüri", "pitch", "slayt", "hazırlık"],
}

DEFAULT_SKILL = "report_section_writer"


def detect_skill(message: str) -> str:
    message_lower = message.lower()
    for skill, keywords in SKILL_KEYWORDS.items():
        for keyword in keywords:
            if keyword in message_lower:
                return skill
    return DEFAULT_SKILL