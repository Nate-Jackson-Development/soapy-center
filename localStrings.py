changelogs = [
    ["9/15/2022", [
        "Slight redesign to authentication area",
        "Made changelog and API reference programattic instead of manually typed",
        "begining work on quarter selector (wont be done until after quarter 2)"
    ]],
    ["12/8/2021", [
        "synced unsynced changes",
        "Fixed schedule overflow"
    ]],
    ["11/15/2021", [
        "uploading changes from 10/20/21 - present",
        "Fixed a mistake on the schedule page"
    ]],
    ["11/10/2021", [
        "Implementing an API reference page",
        "Implemented a working schedule",
        "Fixed persistent signin",
        "Partial fix for edge case with refreshing without a valid session"
    ]],
    ["11/9/2021", [
        "Added changelog",
        "Added persistent signin"
    ]],
    ["10/20/2021", [
        "Fixed course average grade",
        "Added percent sign to course average"
    ]]
]

apiRoutes = [
    # API routes
    ["/api/v1", "GET or POST", "JSON List", "A JSON list of classnames and grade seperated with a colon"],
    ["/api/v1/&lt;classnum&gt;/Assignments", "GET or POST", "JSON List", "A Json list of assignments for the selected class"],
    ["/api/v1/points/&lt;clsnum&gt;", "GET or POST", "JSON list", "A JSON list of the point grade for each assignment in the selected class"],
    ["/api/v1/schedule", "GET or POST", "JSON list", "A JSON list of the users schedule"],
    ["/api/v1/description/lt;classnum&gt;", "GET or POST", "JSON list", "A JSON list of the classes assignment descriptions"],
    # Auth routes
    ["/auth/v1/", "POST", "x-www-form-urlencoded {'username': '*username*', 'password': '*password*'}", "The login endpoint"]
]