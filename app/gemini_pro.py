from .config import get_settings


settings = get_settings()


def generate_story(outline):
    stories = []

    for panel in outline:
        story = {
            "panel": panel.get("panel", len(stories) + 1),
            "title": panel.get("title", ""),
            "narration": panel.get("scene_description", ""),
            "dialogue": ""
        }

        stories.append(story)

    return stories