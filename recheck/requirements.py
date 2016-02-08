from pip.commands import list as pip_list
from pip import req as pip_req
from pip import index as pip_index


def get_requirements_map(requirements_file):
    package_finder = pip_index.PackageFinder(None, None)
    requirements = pip_req.parse_requirements(requirements_file,
                                              finder=package_finder)
    return package_finder, {r.name: r for r in requirements}


def get_oudated_requirements(index_urls=[]):
    cmd = pip_list.ListCommand()
    args = ['--outdated']

    if index_urls:
        index_url, extra_index_urls = index_urls[0], index_urls[1:]
        args.extend(['--index-url', index_url])
        for index_url in extra_index_urls:
            args.extend(['--extra-index-url', index_url])

    options, _ = cmd.parse_args(args)
    return (
        (dist, remote_version_raw, remote_version_parsed)
        for dist, remote_version_raw, remote_version_parsed
        in cmd.find_packages_latests_versions(options)
        if dist.parsed_version != remote_version_parsed
    )
