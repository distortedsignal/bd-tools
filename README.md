## BlueData Tools

A few tools that I'm using at my job at BlueData - feel free to make suggestions!

Here's a function reference, and where to find the tools if you want to modify them.

Tool Name | Location | Explanation 
==========|==========|============
`sshexp`  | sshexp | SSH into hosts using a standard set of credentials
`scpexp`  | scpexp | Send a file to a host using a standard set of credentials
`reset-web` | reset-web | Update python/js/html files on a remote EPIC host with standard credentials
`helper.erl` | helper.erl | Work inside the beam VM on EPIC hosts
`server-setup` | server-setup | Move tools from the local host to a remote host
`ramlize` | ramlize | Run the RAML linter raml-cop against all raml files in our apidocs directory
`py_diff` | py_diff | Run pylint against all python files changed since a certain git ref
`move-beams` | move-beams | Move compiled erlang files to their appropriate places on the EPIC host
`local-api-docs` | local-api-docs | Run a simple python server to display the raml docs locally
`jenkins-build` | jenkins-build | Run a build on the remote jenkins given a standard spec
`force-move` | force-move | Move compiled erlang to the correct place on the EPIC host
`bounce-server` | bounce-server | Restart the local Beam VM
`bd-console` | bd-console | Attach to the running Beam VM
`api-doc-refresh` | api-doc-refresh | Compile and move the api docs
`api-doc-move` | api-doc-move | Move the api docs
`gnp` | .zshgit | Git without the pager
`files-changed` | .zshgit | Show which files have changed compared to current HEAD or a provided ref
`fix-rebase` | .zshgit | When you've borked a rebase, you need to open those files. Open 'em.
`git-recents` | .zshgit | Show which branches you've been working on recently
`grbkd` | .zshgit | Git rebase, but keep the dates correct
`move-changed` | .zshgit | Move beam files that have changed since HEAD or since a given ref to a specified server
