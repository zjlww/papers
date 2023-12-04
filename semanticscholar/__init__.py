"""
Modified implementation of SemanticScholar Wrapper. Remove unused complexity.
"""
from typing import List, Union
import re

from semanticscholar.ApiRequester import ApiRequester
from semanticscholar.Citation import Citation
from semanticscholar.Paper import Paper
from semanticscholar.Reference import Reference

from semanticscholar.ApiRequester import ApiRequester

PaperID = Union[str, int]
FIELDS = [
    "title",
    "corpusId",
    "publicationVenue",
    "year",
    "authors",
    "externalIds",
    "abstract",
    "referenceCount",
    "citationCount",
    "publicationTypes",
    "publicationDate",
]


def transform_paper_id(paper_id: PaperID) -> str:
    """
    Transforms the input paper_id into a specific format based on its pattern.
    If the paper_id matches the pattern of an ARXIV id, it is prefixed with "ARXIV:".
    If the paper_id matches the pattern of a CorpusId, it is prefixed with "CorpusId:".
    Otherwise return as it is.
    """
    if re.match(r"^\d{4}\.\d{4,5}$", str(paper_id)):
        return f"ARXIV:{paper_id}"
    if re.match(r"^\d+$", str(paper_id)):
        return f"CorpusId:{paper_id}"
    return str(paper_id)


class SemanticScholar:
    """
    Main class to retrieve data from Semantic Scholar Graph API
    """

    DEFAULT_API_URL = "https://api.semanticscholar.org"
    DEFAULT_PARTNER_API_URL = "https://partner.semanticscholar.org"

    BASE_PATH_GRAPH = "/graph/v1"

    auth_header = {}

    def __init__(
        self, timeout: int = 10, api_key: str = None, api_url: str = None
    ) -> None:
        if api_url:
            self.api_url = api_url
        else:
            self.api_url = self.DEFAULT_API_URL

        if api_key:
            self.auth_header = {"x-api-key": api_key}
            if not api_url:
                self.api_url = self.DEFAULT_PARTNER_API_URL

        self._timeout = timeout
        self._requester = ApiRequester(self._timeout)

    @property
    def timeout(self) -> int:
        """
        :type: :class:`int`
        """
        return self._timeout

    @timeout.setter
    def timeout(self, timeout: int) -> None:
        self._timeout = timeout
        self._requester.timeout = timeout

    def get_paper(self, paper_id: PaperID, fields: List[str] = FIELDS) -> Paper:
        paper_id = transform_paper_id(paper_id)
        base_url = self.api_url + self.BASE_PATH_GRAPH
        url = f"{base_url}/paper/{paper_id}"

        fields = ",".join(fields)
        parameters = f"&fields={fields}"

        data = self._requester.get_data(url, parameters, self.auth_header)
        paper = Paper(data)

        return paper

    def _get_paper_x(
        self,
        paper_id: str,
        fields: List[str],
        first: int,
        last: int,
        api: str,
    ):
        first = min(first, 9998)
        last = min(last, 9999)
        assert 1 <= last - first <= 1000

        paper_id = transform_paper_id(paper_id)

        base_url = self.api_url + self.BASE_PATH_GRAPH
        url = f"{base_url}/paper/{paper_id}/{api}"

        fields = ",".join(fields)
        parameters = f"&fields={fields}"
        parameters += f"&offset={first}&limit={last - first}"

        results = self._requester.get_data(url, parameters, headers=self.auth_header)
        data = results["data"]
        if api == "citations":
            key = "citingPaper"
        elif api == "references":
            key = "citedPaper"
        else:
            raise RuntimeError(f"API {api} type not supported")
        result_items = [Paper(item[key]) for item in data]
        return result_items

    def get_paper_citations(
        self, paper_id: str, fields: List[str] = FIELDS, first: int = 0, last: int = 100
    ) -> List[Paper]:
        return self._get_paper_x(paper_id, fields, first, last, "citations")

    def get_paper_references(
        self, paper_id: str, fields: List[str] = FIELDS, first: int = 0, last: int = 100
    ) -> List[Paper]:
        return self._get_paper_x(paper_id, fields, first, last, "references")
