# How to Contribute

In order for every developer to work on his own and do not disturb others, we adopt a simple but robust workflow.

Ask Paul the permission to contribute directly in this project.

Read carefully [Github Pull Request documentation](https://help.github.com/articles/creating-a-pull-request/)

### Getting started

First, make sure your local work environment is correctly set using the setting paragraph according to [README.md](https://github.com/goujonpa/bagtrekkin/blob/master/README.md)

Then, check the [`issues`](https://github.com/goujonpa/bagtrekkin/issues) to see which tasks are assigned to you. If you don't have any TO DO, please feel free to discuss it on the web slack channel.

## Roles

Only one person among contributors can push to heroku production server. This person is in charge of running post production tests, deployment, post-production migrations if any and check server is up and running.

## Branches

### Create a dedicated branch

Each new feature should have its own branch following this naming convention : `<username_feature_name>`. To do so, simply create a new branch by checking out:

  ```bash
  $ git checkout -b roddehugo_my_feature
  Switched to a new branch 'roddehugo_my_feature'
  ```

### Work on your branch

While you're working on your feature, you can commit and push to your branch in order to backup your work tree history.

1. Check your work to commit
  ```bash
  $ git status
  On branch roddehugo_my_feature
  Changes not staged for commit:
    (use "git add <file>..." to update what will be committed)
    (use "git checkout -- <file>..." to discard changes in working directory)

          modified:   CONTRIBUTE.md

  no changes added to commit (use "git add" and/or "git commit -a")
  ```

2. Add files or entire directory (`.` in place of `CONTRIBUTE.md`)
  ```bash
  $ git add CONTRIBUTE.md
  ```

3. Commit your changes
  ```bash
  $ git commit
    Adding instructions to CONTRIBUTE
    # Please enter the commit message for your changes. Lines starting
    # with '#' will be ignored, and an empty message aborts the commit.
    # On branch roddehugo_my_feature
    # Changes to be committed:
    #     modified:   CONTRIBUTE.md
    #
  [roddehugo_my_feature 07fafeb] Adding instructions to CONTRIBUTE
   1 file changed, 15 insertions(+), 1 deletion(-)
  ```

4. Push your commits
  ```bash
  $ git push origin roddehugo_my_feature
  Counting objects: 3, done.
  Delta compression using up to 4 threads.
  Compressing objects: 100% (3/3), done.
  Writing objects: 100% (3/3), 546 bytes | 0 bytes/s, done.
  Total 3 (delta 2), reused 0 (delta 0)
  To git@github.com:goujonpa/bagtrekkin.git
   * [new branch]      roddehugo_my_feature -> roddehugo_my_feature
  ```

5. Repeats steps 1 to 4 until your feature is ready to fly over the rainbow

### Make a Pull Request

From now on, your feature is supposed to work well and be fully tested. You can go to Github and submit a pull request on master based on your branch.

1. Create the pull request on Github

  ![Compare and create Pull Request](https://raw.githubusercontent.com/goujonpa/bagtrekkin/master/documentation/img/contribute_1_compare.png)

2. Check everything looks good, add a description if PR needs enlightenments and reference the corresponding issue number by inserting `#num`

  ![Check Pull Request](https://raw.githubusercontent.com/goujonpa/bagtrekkin/master/documentation/img/contribute_2_pr.png)

3. You're not supposed to merge your own PR, it should be your team mate's job

  ![Merge Pull Request](https://raw.githubusercontent.com/goujonpa/bagtrekkin/master/documentation/img/contribute_3_compare.png)

4. Once merge done, you can safely delete the branch


### Retrieve merged work

Once pull request has been accepted, you can switch to master branch and pull down the branch
  ```bash
  $ git checkout master
  ```

You can also delete your branch locally
  ```bash
  $ git branch -d roddehugo_my_feature
  ```

Finaly pull master
  ```bash
  $ git pull origin master
  ```
