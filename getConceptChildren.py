import sys
from typing import Set, Optional
from rdflib import Graph, URIRef, Namespace
from rdflib.namespace import RDF

def get_all_narrower_concepts(graph: Graph, concept_uri: URIRef, visited: Optional[Set[URIRef]] = None) -> Set[URIRef]:
    """
    Recursively extracts all narrower concepts (children) for a given SKOS concept URI.

    Args:
        graph (rdflib.Graph): The RDF graph containing the SKOS thesaurus.
        concept_uri (rdflib.URIRef): The URI of the concept to start from.
        visited (set): A set to keep track of visited URIs to prevent infinite loops
                       in case of circular relationships. Defaults to None.

    Returns:
        set: A set of URIRef objects representing all narrower concepts
             (direct and indirect) of the given concept.
    """
    if visited is None:
        visited = set()

    narrower_concepts: Set[URIRef] = set()

    # Define SKOS namespace
    SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")

    # Find direct narrower concepts
    # The `graph.objects()` method yields all objects for a given subject and predicate.
    for narrower_child_uri in graph.objects(concept_uri, SKOS.narrower):
        # Ensure the child URI is a URIRef (though graph.objects typically returns URIRefs)
        if isinstance(narrower_child_uri, URIRef):
            # Check if the child has already been visited to prevent infinite recursion
            if narrower_child_uri not in visited:
                visited.add(narrower_child_uri)
                narrower_concepts.add(narrower_child_uri)
                # Recursively find narrower concepts of this child
                narrower_concepts.update(get_all_narrower_concepts(graph, narrower_child_uri, visited))

    return narrower_concepts

def main():
    """
    Main function to parse arguments and execute the hierarchy extraction.
    """

    thesaurus_file_path: str = "thesaurus.ttl" #sys.argv[1]
    concept_uri_str: str = "https://www.lassemempel.github.io/terminologies/conservationthesaurus/B51DAF" #sys.argv[2]

    # Create a graph object
    g: Graph = Graph()

    try:
        # Parse the thesaurus file. RDFLib can often guess the format (e.g., 'turtle', 'xml', 'nt').
        # You can also explicitly specify format: g.parse(thesaurus_file_path, format='turtle')
        print(f"Loading thesaurus from: {thesaurus_file_path}")
        g.parse(thesaurus_file_path)
        print("Thesaurus loaded successfully.")
    except Exception as e:
        print(f"Error loading or parsing thesaurus file: {e}")
        sys.exit(1)

    # Convert the input concept URI string to an rdflib.URIRef object
    target_concept_uri: URIRef = URIRef(concept_uri_str)

    # Check if the provided concept URI exists in the graph as a skos:Concept
    SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
    if (target_concept_uri, RDF.type, SKOS.Concept) not in g:
        print(f"Warning: The URI '{concept_uri_str}' does not appear to be a SKOS Concept in the provided thesaurus.")
        # Attempt to proceed anyway, as it might be a valid URI even if not explicitly typed.

    print(f"\nExtracting all narrower concepts for: {target_concept_uri}")
    children: Set[URIRef] = get_all_narrower_concepts(g, target_concept_uri)

    if children:
        print("\nFound the following narrower concepts (including indirect children):")
        print([str(g.value(child_uri, SKOS.prefLabel)) for child_uri in sorted(children)])  # Sort for consistent output
        """
        for child_uri in sorted(list(children)): # Sort for consistent output
            # print prefLabel of the child concept if available
            pref_label = g.value(child_uri, SKOS.prefLabel)
            if pref_label:
                print(f"- {child_uri} (prefLabel: {pref_label})")
            else:
                # If no prefLabel is available, just print the URI
                print(f"- {child_uri}")
        """
    else:
        print("No narrower concepts found for the given URI.")

if __name__ == "__main__":
    main()