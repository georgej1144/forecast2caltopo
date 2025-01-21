
from json import JSONDecodeError

import aiohttp.http
import aiohttp
import pydantic
import datetime

from . import errors
from . import models
from . import LOGGER
from . import __version__


class avy_forecast_getter():

    async def create_session(self):
        self.session = aiohttp.ClientSession()
        return self.session

    def __init__(self) -> None:
        self.headers = {
            "User-Agent": f"balls"
        }
        self.session = None
        # asyncio.run(self.create_session())  # Schedule session creation
    
    # def __del__(self) -> None:
    #     await self.session.close()

    async def _get(self, url: str, params: dict | list | None = None) -> dict:
        """
        Get a URL using this client.

        Meant to be ``CaicURLs`` agnostic, so pass in a full URL.

        Parameters
        ----------
        url : str
            The full URL, in other words, an attr of ``CaicURLs`` + an API endpoint.
        params : dict | None, optional
            Optional URL parameters to pass in - the CAIC
            APIs rely on params, by default None.

        Returns
        -------
        dict
            The return from ``aiohttp.ClientResponse.json`` if, this call, or
            the HTTP request itself, did not throw an error.

        Raises
        ------
        errors.CaicRequestException
            For common HTTP errors, a >400 response status,
            an ``aiohttp.ClientError``, or a ``JSONDecodeError``.
        """

        data = {}
        if self.session == None:
            self.session = await self.create_session()
        try:
            resp = await self.session.get(url, params=params)
            if resp.status >= 400:
                error = await resp.text()
                raise errors.CaicRequestException(
                    f"Error status from CAIC: {resp.status} - {error}"
                )

            data = await resp.json()

        except aiohttp.ClientError as err:
            raise errors.CaicRequestException(
                f"Error connecting to CAIC: {err}"
            ) from err
        except JSONDecodeError as err:
            raise errors.CaicRequestException(
                f"Error decoding CAIC response: {err}"
            ) from err
        else:
            return data
        finally:
            await self.session.close()
            self.session = None


    async def _proxy_get(
            self, proxy_endpoint: str, proxy_uri: str, proxy_params: dict
        ) -> dict | list | None:
        """Get a URL from the avalanche.state.co.us API proxy.

        This is an endpoint that can proxy to other CAIC APIs.

        Parameters
        ----------
        proxy_endpoint : str
            The actual endpoint of the proxy to request, the real URI in the
            HTTP request. Can be any of ``ProxyEndpoints``.
        proxy_uri : str
            The URI used by the proxy in its request to the proxied API.
        proxy_params : dict
            URL parameters to pass in the request to the proxied API.

        Returns
        -------
        dict | list
            The response raw response, or None
        """
        proxy_params_str = "&".join([f"{k}={v}" for k, v in proxy_params.items()])
        params = {"_api_proxy_uri": f"{proxy_uri}?{proxy_params_str}"}
        print("https://avalanche.state.co.us" + proxy_endpoint + "&".join([f"{k}={v}" for k, v in params.items()]))
        return await self._get("https://avalanche.state.co.us" + proxy_endpoint, params=params)

    async def avy_forecast(
            self, date: datetime.datetime|None = None, and_weather: bool = False
        ) -> list[models.AvalancheForecast | models.RegionalDiscussionForecast]:
        """Get the avalanche forecasts as they were on the given date.

        Forecasts cover the date given + the following two days.

        Parameters
        ----------
        date : str
            The date that the avalanche forecast was produced for.

        Returns
        -------
        list[models.AvalancheForecast | models.RegionalDiscussionForecast]
            A list of returned forecasts. The list should contain two types.
            The localized forecast for detailed areas of CO, and the regional
            discussion pieces that cover broader portions of the state.
        """
        params = {}
        if and_weather:
            params["productType"] = "avalancheforecast"
        if date:
            params["datetime"] = date.isoformat() + ("Z" if date.isoformat()[-1] != "Z" else "")

        resp = await self._proxy_get(
            proxy_endpoint="/api-proxy/avid",
            proxy_uri="/products/all",
            proxy_params=params,
        )
        
        ret = []

        if resp:
            try:
                for item in resp:
                    if (
                        isinstance(item, dict)
                        and item.get("type") == "avalancheforecast"
                    ):
                        ret.append(models.AvalancheForecast(**item))
                    else:
                        ret.append(models.RegionalDiscussionForecast(**item))
            except pydantic.ValidationError as err:
                LOGGER.error("Unable to decode forecast response: %s", str(err.errors()))
        return ret


    async def avy_regions(
            self, date: datetime.datetime|None = None, and_weather: bool = False
        ) -> models.RegionFeatureCollection:
        """Get the avalanche forecast regions as they were on the given date.

        Regions have 'id's to match areaIds in AvalancheForecasts.

        Parameters
        ----------
        date : str
            The date that the avalanche forecast was produced for.

        Returns
        -------
        models.RegionFeatureCollection
            A RegionFeatureCollection. This will contain a list of region areas
        """
        params = {}
        if not and_weather:
            params["productType"] = "avalancheforecast"
        if date:
            params["datetime"] = date.isoformat() + ("Z" if date.isoformat()[-1] != "Z" else "")

        resp = await self._proxy_get(
            proxy_endpoint="/api-proxy/avid",
            proxy_uri="/products/all/area",
            proxy_params=params,
        )
        
        ret = None

        if resp:
            try:
                if (
                    isinstance(resp, dict)
                    and resp.get("type") == "FeatureCollection"
                ):
                    ret = models.RegionFeatureCollection(**resp)
            except pydantic.ValidationError as err:
                LOGGER.error("Unable to decode forecast response: %s", str(err.errors()))
        return ret
