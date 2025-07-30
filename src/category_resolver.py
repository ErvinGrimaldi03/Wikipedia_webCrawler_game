# category_resolver.py
import json
from functools import lru_cache


class CategoryResolver:
    """
    Resolves Wikipedia categories, potentially mapping to a hierarchical taxonomy
    and inferring broader topics from infobox data and categories.
    """

    def __init__(self, category_mapping_file: str = None):
        """
        Initializes the CategoryResolver.
        Args:
            category_mapping_file (str, optional): Path to a JSON file containing 
                                                   a pre-built category hierarchy.
                                                   Defaults to None, in which case
                                                   _fetch_category_parents_from_wiki
                                                   is used (conceptually).
        """
        self.category_tree = {}  # {category_name: [parent_categories_names]}
        if category_mapping_file:
            try:
                with open(category_mapping_file, 'r', encoding='utf-8') as f:
                    self.category_tree = json.load(f)
                print(f"Loaded category tree from {category_mapping_file}")
            except FileNotFoundError:
                print(f"Warning: Category mapping file '{category_mapping_file}' not found. "
                      "Category resolution will be limited to direct categories unless manually overridden.")
            except json.JSONDecodeError:
                print(f"Error decoding JSON from '{category_mapping_file}'. Category resolution will be limited.")
                self.category_tree = {}

    @lru_cache(maxsize=100000)  # Cache to avoid repeated lookups for category parents
    def _get_parents_from_tree(self, category_name: str) -> list[str]:
        """
        Retrieves direct parent categories from the loaded category_tree.
        """
        # Wikipedia categories are usually like "Category:Science"
        # We need to make sure we're looking up the consistent format.
        # Clean the category name for lookup.
        cleaned_cat_name = category_name.replace("Category:", "").strip()

        # In a real comprehensive system, this tree would be very deep.
        # For now, it's a simple lookup.
        parents = self.category_tree.get(cleaned_cat_name, [])
        return [f"Category:{p}" for p in parents]  # Return in "Category:X" format

    def _recursively_resolve_parents(self, category_name: str, max_depth: int = 3, current_depth: int = 0) -> set[str]:
        """
        Recursively finds all ancestor categories up to a certain depth.
        """
        if current_depth >= max_depth:
            return set()

        all_parents = set()
        direct_parents = self._get_parents_from_tree(category_name)

        for parent in direct_parents:
            all_parents.add(parent)
            all_parents.update(self._recursively_resolve_parents(parent, max_depth, current_depth + 1))

        return all_parents

    def resolve_categories_and_hierarchy(self, raw_categories: list[str], max_depth: int = 2) -> list[str]:
        """
        Takes a list of raw Wikipedia categories and returns a more refined
        list, including inferred parent categories based on a loaded hierarchy.
        """
        resolved = set()
        for cat in raw_categories:
            resolved.add(cat)
            # Add parents recursively based on the pre-built category_tree
            resolved.update(self._recursively_resolve_parents(cat, max_depth=max_depth))

        # Remove "Category:" prefix for cleaner topic names
        return sorted([c.replace("Category:", "").strip() for c in resolved])

    # --- FIX STARTS HERE ---
    def get_canonical_topics(self, raw_categories: list[str], infobox_data: dict, article_title: str) -> list[str]:
        # --- FIX ENDS HERE ---
        """
        Combines resolved categories and infobox data to infer canonical, high-level topics.
        This uses heuristics and a mapping strategy.

        Args:
            raw_categories (list[str]): List of raw categories from the Wikipedia page.
            infobox_data (dict): Dictionary of infobox key-value pairs.
            article_title (str): The title of the Wikipedia article.

        Returns:
            list[str]: A sorted list of inferred canonical topics.
        """
        topics = set()

        # Step 1: Infer from Infobox data (often very strong signals)
        # These mappings are examples and would be extensively refined.
        if 'occupation' in infobox_data: topics.add("Person")
        if 'genre' in infobox_data: topics.add("Art & Culture")  # Broad
        if 'developer' in infobox_data or 'publisher' in infobox_data: topics.add("Technology")
        if 'country' in infobox_data or 'capital' in infobox_data: topics.add("Geography")
        if 'director' in infobox_data and 'starring' in infobox_data: topics.add("Film")
        if 'artist' in infobox_data and 'album' in infobox_data: topics.add("Music")
        if 'scientific_name' in infobox_data: topics.add("Biology")
        if 'president' in infobox_data or 'party' in infobox_data: topics.add("Politics")
        if 'author' in infobox_data and 'genre' in infobox_data: topics.add("Literature")
        if 'sport' in infobox_data and 'league' in infobox_data: topics.add("Sports")
        if 'type' in infobox_data and 'manufacturer' in infobox_data: topics.add("Product/Technology")
        if 'diseases' in infobox_data or 'medical_condition' in infobox_data: topics.add("Health/Medicine")
        if 'discovery' in infobox_data or 'element' in infobox_data: topics.add("Science")

        # Step 2: Map raw Wikipedia categories to broader, more canonical topics
        # This mapping would be extensive and refined over time based on analysis of Wikipedia's categories.
        # Example mapping (highly simplified):
        category_to_topic_map = {
            "Video game characters": "Gaming",
            "Fictional characters": "Fiction",
            "American singers": "Music",
            "Pop musicians": "Music",
            "Historical figures": "History",
            "Scientists": "Science",
            "Flora": "Biology/Nature",
            "Fauna": "Biology/Nature",
            "Computer science": "Technology",
            "Programming languages": "Technology",
            "Countries": "Geography",
            "Cities": "Geography",
            "Diseases": "Health/Medicine",
            "Anatomy": "Health/Medicine",
            "Films": "Film",
            "Albums": "Music",
            "Battles": "History",
            "Wars": "History",
            "Philosophers": "Philosophy",
            "Religions": "Religion",
            "Sportspeople": "Sports",
            "Companies": "Business",
            "Organisations": "Organizations",
            "Education": "Education",
            "Mathematics": "Mathematics",
            "Literature": "Literature",
            "Art": "Art",
            # ... and many more. This would be dynamically built or loaded.
        }

        # First, add the resolved raw categories themselves, cleaned.
        resolved_hierarchical_categories = self.resolve_categories_and_hierarchy(raw_categories)
        for cat in resolved_hierarchical_categories:
            topics.add(cat)  # Add the cleaned category name directly

        # Then, apply the mapping to get broader canonical topics
        for cat in raw_categories:  # Use raw categories for mapping lookup initially
            cleaned_cat = cat.replace("Category:", "").strip()
            if cleaned_cat in category_to_topic_map:
                topics.add(category_to_topic_map[cleaned_cat])

        # Step 3: Refinement and Deduplication (Heuristics)
        # Remove very general categories if more specific ones exist.
        # This requires careful thought and iteration.

        # Example: If a more specific technology term exists, remove generic "Technology" if desired
        if "Gaming" in topics or "Software" in topics or "Engineering" in topics:
            topics.discard("Technology")  # Example: prefer specific over general

        if ("Film" in topics or "Music" in topics or "Literature" in topics) and "Art & Culture" in topics:
            topics.discard("Art & Culture")

        if "Biology" in topics or "Physics" in topics or "Chemistry" in topics:
            topics.discard("Science")  # Prefer specific science fields

        # Add title keywords to topics if they provide extra context (e.g., "The History of X")
        # This is a very light touch, as lead_text covers most.
        title_keywords = article_title.lower().split()
        if 'history' in title_keywords: topics.add('History')
        if 'science' in title_keywords: topics.add('Science')

        # Ensure "People" is added if a person's infobox is detected
        if 'occupation' in infobox_data:
            topics.add("People")

        return sorted(list(topics))  # Return sorted list for consistent output